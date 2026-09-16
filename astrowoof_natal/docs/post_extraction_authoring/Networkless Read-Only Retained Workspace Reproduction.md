# Networkless Read-Only Retained Workspace Reproduction

```yaml
status: accepted
owner: semantic-basis-extractor
scope: provider-free forensic execution of an authorized retained native workspace
last_reviewed: 2026-09-15
```

## Purpose

Use this pattern when static inspection is insufficient and an exact retained
workspace must be exercised through public SBE readers or deterministic local
builders. A verified disposable extraction is mounted into an ephemeral Docker
container at the workspace's original contract-bound absolute root. The mount is
read-only, the container has no network, and the container itself cannot write
outside a bounded temporary filesystem.

This creates a sealed forensic replay environment. It permits native code to read
and evaluate historical bytes without granting authority to resume, repair,
reconcile, retry, publish, call a provider, or mutate either the retained object or
the extracted copy.

This procedure does **not** make an R2 read permissible. Object coordinates and
the exact HEAD/GET budget must already be separately authorized. Acquisition,
verification, extraction, and execution are distinct gates.

## Why the exact logical root matters

SBE workspaces bind their stable logical absolute root in native evidence. A
random host extraction path is therefore not a valid execution root. Passing that
path directly should fail the stable-root check and proves only that relocation is
rejected.

Docker supplies the missing namespace boundary: mount the disposable host
extraction at the exact Linux path recorded by the workspace contract. SBE then
sees the original logical root while Docker keeps the host copy read-only. This is
forensic path recreation, not supported workspace rebasing.

An intentionally wrong mount can be useful as a negative control. Record its
stable-root refusal separately and never mistake it for the incident under study.

## Required gates

### 1. Freeze the question

Before acquisition, record:

- the exact run, checkpoint generation, object key, ETag, byte size, archive
  digest, inventory digest, logical root, and native result ID;
- the public read-only function or deterministic helper to invoke;
- the expected stdout/result shape and prohibited effects; and
- the separate owner authorization for the bounded object reads.

Prefer one narrow stage per container. Do not run a whole coordinator merely
because the workspace is available.

### 2. Acquire exactly the authorized object

Use one conditional HEAD and one ETag-bound, byte-bounded GET only when that exact
budget was approved. Do not list, discover a newer checkpoint, retry a failed GET,
or access an alternate key without new authorization. Record a receipt and treat
the budget as consumed.

### 3. Verify before extraction

Verify the downloaded archive before allowing its paths onto the host:

- exact object size, ETag binding, and archive SHA-256;
- no duplicate members;
- no absolute, drive-qualified, parent-traversal, or backslash-confused paths;
- no symbolic or hard links;
- expected archive type rather than filename suffix alone; and
- after extraction, every manifest member's relative path, byte count, SHA-256,
  and canonical inventory digest.

Extract only into a new disposable directory outside the repository and outside
every native workspace. Never extract over an existing run.

### 4. Freeze the image and code

Use an already-present image when possible. Record its immutable image digest,
Python version, SBE wheel/source identity, and any API source identity used in the
reproduction. Do not pull an image or install dependencies during the forensic
run. Those operations require network and make the environment harder to attest.

Mount code and installed-wheel material read-only. Do not pass cloud, provider,
Better Stack, database, or deployment credentials into the container.

### 5. Apply the isolation envelope

The minimum adopted envelope is:

- `--network none`;
- `--read-only` for the container root filesystem;
- `--mount ... readonly` for the extracted workspace and source inputs;
- `--cap-drop ALL`;
- `--security-opt no-new-privileges`;
- a size-bounded `tmpfs` for the small amount of scratch space Python requires;
- no Docker socket, host root, user profile, credential, or unrelated workspace
  mount; and
- `--rm` so the container is discarded after output is collected.

Process, memory, CPU, and wall-clock limits should also be applied when the chosen
image and invocation support them. They bound resource use; they do not replace
the read-only and networkless controls.

### 6. Prove the observed effects

Capture only the minimum diagnostic output. After execution, prove:

- the container exited and was removed;
- no network or provider operation was possible;
- the host extraction still matches its pre-run inventory digest;
- no API, R2, database, Better Stack, or native workspace mutation occurred; and
- the result came from the exact requested native result ID, not latest-result
  discovery.

Delete disposable copies only under the investigation's retention policy. Their
existence is not authority for another run.

## Sanitized PowerShell example

The following illustrates the shape of an exact-root, read-only call. Replace the
placeholders only from the approved coordinate packet and an already-present image.
It deliberately passes no credentials and grants no writable bind mount.

```powershell
$forensicWorkspace = 'C:\tmp\retained-workspace\sbe'
$contractRoot = '/work/runs/workspace-00000000-0000-0000-0000-000000000000/sbe'
$sourceRoot = 'C:\dev\github\semantic-basis-extractor'
$imageRef = 'local-sbe-forensics@sha256:<verified-image-digest>'
$resultId = 'sbe-result-v0.2:<exact-result-id>'

docker run --rm `
  --network none `
  --read-only `
  --cap-drop ALL `
  --security-opt no-new-privileges `
  --pids-limit 128 `
  --memory 1g `
  --cpus 1 `
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m `
  --mount "type=bind,source=$forensicWorkspace,target=$contractRoot,readonly" `
  --mount "type=bind,source=$sourceRoot,target=/opt/sbe-source,readonly" `
  --workdir /opt/sbe-source `
  $imageRef `
  python -m <read-only-diagnostic-module> `
    --workspace $contractRoot `
    --result-id $resultId
```

If the image lacks a non-root user, prefer adding the image's established numeric
runtime UID/GID with `--user`; do not guess an identity that makes required files
unreadable. A diagnostic module must itself be read-only and provider-free. Docker
is an additional containment layer, not evidence that an arbitrary command is safe.

## Useful staged matrix

When a broad exported helper fails, isolate its phases in fresh containers:

| Stage | Example question |
| --- | --- |
| Exact result reader | Does the exact result/receipt/snapshot join validate? |
| Eligibility reader | Which typed native route is selected? |
| Evidence collector | Does retained evidence produce data or a typed absence? |
| SBE capture builder | Does packet/status construction return or raise? |
| API envelope builder | Can the typed SBE result be serialized locally? |
| Request preflight | Can deterministic compression/size checks complete without posting? |

Fresh containers keep one slow or stateful import from obscuring later stages and
make each exit independently attributable. A timeout is not a functional failure;
rerun only when the local execution plan permits it, never by spending another R2
read.

## What this pattern has already established

The method first became especially useful in the September 2026 terminal-observer
investigations:

- Aldine/Moxon cleared the exact native reader, capture construction, API envelope,
  and deterministic request preflight, moving ownership to the API live-post
  boundary.
- Bodoni/Turing showed that exact-root public capture returned a valid typed
  `contradictory_native_evidence` status rather than reproducing the live exception.
- Bembo/Morris separately exercised exact reader, eligibility, evidence collection,
  implementation capture, and package export; neither retained workspace reproduced
  the live `TypeError`.

Those were valuable negative reproductions. The environment did not force the
historical failure to recur; it proved which deterministic boundaries were sound on
the exact retained bytes.

## Claim limits

This procedure can prove behavior of the verified archive under the recorded local
image, code, interpreter, and invocation. It cannot prove that a destroyed live
container had identical transient bytes, imports, environment, timing, memory, or
deployment configuration. It cannot authorize a transition, infer a missing
provider operation, or convert retained evidence into a resumable checkpoint.

Treat differences between live and replayed behavior as localization evidence, not
permission to weaken native validation.
