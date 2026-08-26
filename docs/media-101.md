# media-101 — a translation table, not a textbook

For senior engineers who have never touched media services. Each entry maps a
media concept onto a systems concept you already own. If an entry wants to be
longer than a paragraph, it becomes an ADR or a journal section instead.

| Media term | You already know this as | The one thing to remember |
|---|---|---|
| **Mezzanine** | The source artifact / master build input | High-bitrate original everything derives from. In this repo: the S3 object the pipeline starts from. |
| **Transcoding / ABR ladder** | Cross-compilation for heterogeneous targets | One source, N builds, each tuned to a device/network profile. The "ladder" is your build matrix. |
| **MediaConvert** | The batch compiler | File in, renditions out, billed per normalized output minute. Its job spec is JSON; you'll feel at home. |
| **HLS manifest (.m3u8)** | A plain-text index file | `curl` it and the ladder is right there as text. The single most trust-building artifact in the chain. |
| **Segments** | Chunked transfer with seekability | Short .ts/.mp4 pieces; why live and VOD share a delivery path. |
| **MediaPackage** | Origin server + content-negotiation middleware | One ingest, HLS or DASH out; DRM applied at the origin, not baked into assets. |
| **SCTE-35** | An event bus inside the stream | A webhook that travels with the bits. Ad insertion stops being exotic once you hear this. |
| **MediaTailor** | Per-request middleware that rewrites the manifest | Splices ads server-side, so the player sees one continuous video. Executive translation: revenue. |
| **MediaLive** | The streaming counterpart to the batch compiler | Always-on process billed per channel-hour — which is why this repo only runs it inside `make event-window`. |
| **QVBR** | An SLO for quality instead of a bitrate quota | "Hit this perceptual quality, spend the fewest bits doing it." The knob the agent mostly turns. |
| **VMAF** | A computable assertion about perceptual quality | Makes "did quality drop?" CI-gateable, the way tests gate correctness. |
| **CMCD** | RUM for video players | Standardized client beacons; closes the loop from delivery back to measurement. |
| **CDN (CloudFront)** | The cache tier | Same mental model as any edge cache; video is just very cacheable. |
