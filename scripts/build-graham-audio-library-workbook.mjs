import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const inputDir = process.argv[2];
const outputPath = process.argv[3];
if (!inputDir || !outputPath) throw new Error("Usage: node build-graham-audio-library-workbook.mjs <input-dir> <output.xlsx>");

async function csvRows(name) {
  const text = await fs.readFile(`${inputDir}/${name}`, "utf8");
  if (!text.trim()) return [];
  const temp = await Workbook.fromCSV(text, { sheetName: "Data" });
  return temp.worksheets.getItem("Data").getUsedRange(true).values;
}

function objects(matrix) {
  if (!matrix.length) return [];
  const headers = matrix[0].map(String);
  return matrix.slice(1).map(row => Object.fromEntries(headers.map((h, i) => [h, row[i] ?? ""])));
}

function colLetter(index) {
  let n = index + 1, result = "";
  while (n) { n--; result = String.fromCharCode(65 + (n % 26)) + result; n = Math.floor(n / 26); }
  return result;
}

const files = {
  folders: "graham-library-folder-candidates.csv",
  filesets: "graham-library-fileset-candidates.csv",
  longAudio: "graham-library-long-audio-candidates.csv",
  evidence: "graham-library-keyword-evidence.csv",
  containers: "graham-library-large-container-candidates.csv",
};
const matrices = Object.fromEntries(await Promise.all(Object.entries(files).map(async ([k, v]) => [k, await csvRows(v)])));
const rows = Object.fromEntries(Object.entries(matrices).map(([k, v]) => [k, objects(v)]));

const wb = Workbook.create();
const font = "Arial";
const navy = "#23344D";
const blue = "#DCE6F1";
const amber = "#FFF2CC";
const pale = "#F3F6F9";

function titleBlock(sheet, title, subtitle, width) {
  sheet.showGridLines = false;
  sheet.getRange(`A1:${colLetter(width - 1)}1`).format.borders = { bottom: { style: "thin", color: "#8292A8" } };
  sheet.getRange("A1").values = [[title]];
  sheet.getRange("A1").format.font = { name: font, size: 16, bold: true, color: navy };
  sheet.getRange("A2").values = [[subtitle]];
  sheet.getRange(`A2:${colLetter(width - 1)}2`).format.font = { name: font, size: 10, italic: true, color: "#566273" };
}

function addTableSheet(name, matrix, title, subtitle, widths = {}) {
  const sheet = wb.worksheets.add(name);
  const safe = matrix.length ? matrix : [["No candidates"]];
  const cols = safe[0].length;
  titleBlock(sheet, title, subtitle, cols);
  sheet.getRangeByIndexes(3, 0, safe.length, cols).values = safe;
  const header = sheet.getRangeByIndexes(3, 0, 1, cols);
  header.format = { fill: navy, font: { name: font, size: 10, bold: true, color: "#FFFFFF" }, wrapText: true, verticalAlignment: "center" };
  header.format.rowHeight = 32;
  if (safe.length > 1) {
    const body = sheet.getRangeByIndexes(4, 0, safe.length - 1, cols);
    body.format.font = { name: font, size: 10, color: "#1F2937" };
    body.format.verticalAlignment = "top";
    body.format.wrapText = true;
    sheet.tables.add(`A4:${colLetter(cols - 1)}${safe.length + 3}`, true, `${name.replace(/[^A-Za-z0-9]/g, "")}Table`).style = "TableStyleMedium2";
  }
  sheet.freezePanes.freezeRows(4);
  safe[0].forEach((h, i) => { sheet.getRangeByIndexes(0, i, safe.length + 3, 1).format.columnWidth = widths[h] ?? 16; });
  return sheet;
}

const summary = wb.worksheets.add("Summary");
titleBlock(summary, "Graham audio library candidates", "D: drive inventory plus the January 2013 migration archive. iTunes results are deliberately treated as a backstop.", 8);
summary.getRange("A4:B9").values = [
  ["Finding", "Result"],
  ["Exact Graham matches", 0],
  ["Audio files assessed", 16921],
  ["Long audio files (20+ min)", rows.longAudio.length],
  ["Keyword-evidence tracks", rows.evidence.length],
  ["Large opaque containers", rows.containers.length],
];
summary.getRange("A4:B4").format = { fill: navy, font: { name: font, bold: true, color: "#FFFFFF" } };
summary.getRange("A5:B9").format.font = { name: font, size: 11 };
summary.getRange("A11:H11").values = [["Priority", "Candidate", "Type", "Audio files", "Long files", "Hours", "Why it stands out", "Caveat"]];
const namedSets = rows.filesets.filter(r => !/^D:\\?$|^D:\\My Music$|\\iTunes\\iTunes Music$|\\iTunes$/.test(String(r.Folder))).slice(0, 10);
const leadRows = namedSets.map(r => [r.LocationPriority, r.Folder, "Folder/fileset", Number(r.AudioFiles), Number(r.LongAudioFiles), Number(r.TotalHours), r.Evidence, r.LocationPriority === "iTunes backstop" ? "Inside previously reviewed iTunes tree" : "Ownership not proven"]);
for (const r of rows.containers) leadRows.push(["Non-iTunes priority", r.FullName, "Opaque archive", "", "", "", r.Evidence, "Requires archive index to identify contents"]);
summary.getRangeByIndexes(11, 0, leadRows.length, 8).values = leadRows;
summary.getRange("A11:H11").format = { fill: navy, font: { name: font, size: 10, bold: true, color: "#FFFFFF" }, wrapText: true };
summary.getRangeByIndexes(11, 0, leadRows.length + 1, 8).format.wrapText = true;
summary.getRangeByIndexes(11, 0, leadRows.length + 1, 8).format.verticalAlignment = "top";
summary.getRangeByIndexes(11, 0, leadRows.length + 1, 8).format.rowHeight = 38;
summary.getRange("A4:B9").format.borders = { preset: "outside", style: "thin", color: "#AAB4C3" };
summary.getRange("A13:H13").format.fill = amber;
summary.getRange("A22:H22").format.fill = amber;
summary.getRange("A25:H27").values = [
  ["Interpretation", "", "", "", "", "", "", ""],
  ["No path, filename, or embedded audio tag contains Graham. The named DnB/breaks candidates all resolve to the iTunes tree. The BKF remains the principal non-iTunes unknown because its internal ownership cannot be inferred from the outer filename.", "", "", "", "", "", "", ""],
  ["Scores are triage aids, not evidence of ownership. Duplicate copies and ancestor folders can inflate totals; use the fileset and long-audio tabs for actionable paths.", "", "", "", "", "", "", ""],
];
summary.getRange("A25:H25").format = { fill: blue, font: { name: font, bold: true, color: navy } };
summary.getRange("A26:H27").format = { fill: pale, font: { name: font, size: 10 }, wrapText: true };
summary.getRange("A26:H26").merge(true);
summary.getRange("A27:H27").merge(true);
summary.getRange("A26:H27").format.rowHeight = 44;
summary.freezePanes.freezeRows(11);
[28, 62, 18, 12, 12, 10, 44, 38].forEach((w, i) => summary.getRangeByIndexes(0, i, 27, 1).format.columnWidth = w);

addTableSheet("Filesets", matrices.filesets, "Folder-level filesets", "Immediate audio folders ranked by explicit Graham, DnB, breaks, set/session language, and long-track evidence. Non-iTunes first.", { Folder: 68, Evidence: 38, AlbumValues: 38, Artists: 34, LocationPriority: 18 });
addTableSheet("Long audio", matrices.longAudio, "Long single audio files", "Audio lasting at least 20 minutes. These are strong candidates for DJ mixes, radio captures, and continuous sets.", { FullName: 70, AccessiblePath: 70, Title: 28, Artist: 24, Album: 28, Evidence: 32, LocationPriority: 18 });
addTableSheet("Named evidence", matrices.evidence, "Keyword evidence", "Tracks whose path or tags contain Graham, DnB/drum-and-bass, breaks/breakbeat, or set/session language.", { FullName: 70, AccessiblePath: 70, Title: 30, Artist: 25, Album: 34, MatchReasons: 34 });
addTableSheet("Folder rollups", matrices.folders, "Folder and ancestor rollups", "Broader folder clusters. Ancestors can duplicate counts, so use this tab to locate collections rather than estimate unique totals.", { Folder: 70, Evidence: 38, Formats: 35, LeadingGenres: 30, LocationPriority: 18 });
addTableSheet("Large containers", matrices.containers, "Large opaque containers", "Archives and backup containers over 100 MB whose contents may not be represented in ordinary file manifests.", { FullName: 70, Evidence: 52 });

for (const sheet of wb.worksheets.items) {
  const used = sheet.getUsedRange(true);
  used.format.font.name = font;
}

const check = await wb.inspect({ kind: "table", range: "Summary!A1:H27", include: "values,formulas", tableMaxRows: 30, tableMaxCols: 10 });
console.log(check.ndjson);
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "final formula error scan" });
console.log(errors.ndjson);

await fs.mkdir(inputDir, { recursive: true });
for (const sheetName of ["Summary", "Filesets", "Long audio", "Named evidence", "Folder rollups", "Large containers"]) {
  const preview = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(`${inputDir}/preview-${sheetName.replace(/ /g, "-").toLowerCase()}.png`, new Uint8Array(await preview.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(outputPath);
console.log(`SAVED=${outputPath}`);
