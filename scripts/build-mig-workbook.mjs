import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = "D:/2026 Extracted Archives/External Drive Jan 2013 Windows Easy Transfer";
const outPath = `${root}/January 2013 archive inventory.xlsx`;

async function csvValues(path, sheetName) {
  const csv = await fs.readFile(path, "utf8");
  if (!csv.trim()) return [];
  const temp = await Workbook.fromCSV(csv, { sheetName });
  return temp.worksheets.getItem(sheetName).getUsedRange().values;
}

const files = await csvValues(`${root}/archive-manifest.csv`, "FilesImport");
const audio = await csvValues(`${root}/audio-manifest.csv`, "AudioImport");
const corrupt = await csvValues(`${root}/corrupt-or-unrecoverable-items.csv`, "CorruptImport");
const candidateText = await fs.readFile(`${root}/careless-whisper-candidates.csv`, "utf8");
const candidates = candidateText.trim() ? await csvValues(`${root}/careless-whisper-candidates.csv`, "CandidatesImport") : [];

const wb = Workbook.create();
const summary = wb.worksheets.add("Summary");
const candidateSheet = wb.worksheets.add("Candidates");
const audioSheet = wb.worksheets.add("Audio");
const filesSheet = wb.worksheets.add("All files");
const corruptSheet = wb.worksheets.add("Recovery issues");

const bodyFont = { name: "Arial", size: 10, color: "#1F2937" };
const headerFormat = { fill: "#243447", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" }, verticalAlignment: "center" };

summary.showGridLines = false;
summary.getRange("A1:B1").merge();
summary.getRange("A1").values = [["January 2013 Windows Easy Transfer archive"]];
summary.getRange("A1").format.font = { name: "Arial", size: 16, bold: true, color: "#172033" };
summary.getRange("A2:B2").merge();
summary.getRange("A2").values = [["Recovered from Windows Easy Transfer - Items from old computer.MIG"]];
summary.getRange("A2").format.font = { name: "Arial", size: 10, italic: true, color: "#5B6472" };
summary.getRange("A4:B10").values = [
  ["Metric", "Result"],
  ["Logical recovered files", 20286],
  ["Logical recovered size (GB)", 55.548357003],
  ["Audio files with metadata inspected", 419],
  ["Careless Whisper candidates", candidates.length > 1 ? candidates.length - 1 : 0],
  ["Known corrupt named files", 1],
  ["Known corrupt unnamed members", 1],
];
summary.getRange("A4:B4").format = headerFormat;
summary.getRange("A5:B10").format.font = bodyFont;
summary.getRange("B5").format.numberFormat = "#,##0";
summary.getRange("B6").format.numberFormat = "0.00";
summary.getRange("B7:B10").format.numberFormat = "#,##0";
summary.getRange("A12:B15").values = [
  ["Finding", "No filename or readable embedded tag matched Careless Whisper, George Michael, or Wham."],
  ["Recovery method", "Microsoft USMT full extraction, plus a second pass excluding *.MOD after one damaged MOD payload crashed USMT."],
  ["Logical catalog rule", "Non-MOD files use the complete second tree; healthy MOD files use the first tree."],
  ["Original archive", "E:\\Transfer\\Windows Easy Transfer - Items from old computer.MIG"],
];
summary.getRange("A12:A15").format.font = { name: "Arial", size: 10, bold: true, color: "#172033" };
summary.getRange("B12:B15").format = { font: bodyFont, wrapText: true };
summary.getRange("A1:B15").format.rowHeight = 21;
summary.getRange("A:A").format.columnWidth = 30;
summary.getRange("B:B").format.columnWidth = 92;

candidateSheet.showGridLines = false;
if (candidates.length > 1) {
  candidateSheet.getRange("A1").write(candidates);
} else {
  candidateSheet.getRange("A1:H2").values = [
    ["Candidate score", "Reasons", "Title", "Artist", "Album", "Original path", "Recovered path", "Result"],
    [0, "", "", "", "", "", "", "No plausible candidates found in filenames or readable embedded tags."],
  ];
}
candidateSheet.getUsedRange().format.font = bodyFont;
candidateSheet.getRangeByIndexes(0, 0, 1, candidateSheet.getUsedRange().columnCount).format = headerFormat;
candidateSheet.freezePanes.freezeRows(1);
candidateSheet.getUsedRange().format.autofitColumns();
candidateSheet.getUsedRange().format.autofitRows();

audioSheet.getRange("A1").write(audio);
audioSheet.getUsedRange().format.font = bodyFont;
audioSheet.getRangeByIndexes(0, 0, 1, audio[0].length).format = headerFormat;
audioSheet.freezePanes.freezeRows(1);
audioSheet.getUsedRange().format.autofitColumns();
for (const col of [0,1]) audioSheet.getRangeByIndexes(0,col,audio.length,1).format.columnWidth = col === 0 ? 70 : 90;

filesSheet.getRange("A1").write(files);
filesSheet.getUsedRange().format.font = bodyFont;
filesSheet.getRangeByIndexes(0, 0, 1, files[0].length).format = headerFormat;
filesSheet.freezePanes.freezeRows(1);
filesSheet.getUsedRange().format.autofitColumns();
filesSheet.getRangeByIndexes(0,0,files.length,1).format.columnWidth = 85;
filesSheet.getRangeByIndexes(0,1,files.length,1).format.columnWidth = 75;
filesSheet.getRangeByIndexes(0,2,files.length,1).format.columnWidth = 95;

corruptSheet.getRange("A1").write(corrupt);
corruptSheet.getUsedRange().format.font = bodyFont;
corruptSheet.getRangeByIndexes(0, 0, 1, corrupt[0].length).format = headerFormat;
corruptSheet.freezePanes.freezeRows(1);
corruptSheet.getUsedRange().format.autofitColumns();
corruptSheet.getUsedRange().format.autofitRows();

const summaryCheck = await wb.inspect({ kind: "table", sheetId: "Summary", range: "A1:B15", include: "values,formulas", tableMaxRows: 20, tableMaxCols: 4 });
console.log(summaryCheck.ndjson);
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" });
console.log(errors.ndjson);
const preview = await wb.render({ sheetName: "Summary", range: "A1:B15", scale: 1.5, format: "png" });
await fs.writeFile(`${root}/catalog-summary-preview.png`, new Uint8Array(await preview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(outPath);
console.log(outPath);
