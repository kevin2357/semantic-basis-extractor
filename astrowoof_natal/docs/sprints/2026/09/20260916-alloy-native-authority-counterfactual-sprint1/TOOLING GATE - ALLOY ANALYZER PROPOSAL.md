# Tooling Gate — Alloy Analyzer Proposal

Status: proposed only; no download, installation, or execution has occurred.

## Local inventory

This host currently has no `alloy` command, Alloy Analyzer JAR, or `java` command
available in the inspected local tool/cache locations.

## Proposed acquisition

Use the official AlloyTools GitHub release `v6.2.0`, specifically the Windows x64
archive:

```text
https://github.com/AlloyTools/org.alloytools.alloy/releases/download/v6.2.0/alloy-6.2.0-windows-amd64.zip
```

The official release describes Alloy 6.2.0 as providing both a JAR and OS-specific
packages, including a Windows AMD64 archive. Its release notes document a CLI via
`java -jar alloy.jar help`. The release page reports the Windows AMD64 archive as
approximately 46.2 MB.

## Proposed safe use

1. Download only the stated archive into `C:\tmp\alloy-6.2.0-windows-amd64.zip`.
2. Compute SHA-256 locally and record the actual bytes/digest in sprint evidence.
3. Extract only into a new disposable `C:\tmp\alloy-6.2.0\` directory.
4. Inspect its manifest/help/version before executing any model.
5. Run only the new local `.als` files against bounded scopes, with no model command
   that performs network, provider, database, R2, deployment, or repository mutation.
6. Leave the tool outside the repository and do not add it to `PATH`, install a
   package manager dependency, or commit binaries.

## Why this is proportionate

The archive is an external binary distribution, so its acquisition is a meaningful
tooling change even though the planned analysis is offline and disposable. The model
itself can be versioned in the repository; the Analyzer must remain temporary.

## Requested owner authorization

Authorize exactly one download of the above official archive, its extraction under
`C:\tmp`, and local offline execution of the new bounded native-authority `.als`
models. No other download or installation is included.

