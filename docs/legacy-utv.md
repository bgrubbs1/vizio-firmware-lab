# Legacy UpdateLogic UTV

Vizio has shipped more than one format with the UTV extension. The parser in this repository identifies the legacy format by its 16-byte magic and validates record lengths against the whole file.

| Offset | Size | Field |
| --- | ---: | --- |
| 0x00 | 16 | Magic, ASCII BDC, CDB, BDC, CDB separated and terminated by tabs |
| 0x10 | 1 | Clear header version |
| 0x11 | 1 | Key header version |
| 0x12 | 1 | Key header type |
| 0x13 | 1 | Reserved byte |
| 0x14 | 4 | Vendor/platform ID, little-endian |
| 0x18 | 4 | Model group ID, little-endian |
| 0x1c | 4 | Total record length, little-endian |

The open-source extractor unixtract describes a 256-byte RSA-transformed key header for its supported legacy type 3 format, then an encrypted body. The first decoded body supplies the component directory. The upstream extractor uses a different path for Qterics images, which use signed metadata and a different payload scheme.

A matching round-trip hash shows the header layout accounts for the bytes used to recreate the container with its original opaque bodies. Extracting components or creating an updater-accepted modified image requires separate validation.

## References

- [unixtract format implementations](https://github.com/theubusu/unixtract/tree/main/src/formats)
- [Independent legacy UTV header parser](https://gist.github.com/theubusu/13e12513fedd3b52c88d5e9b1a4cf1ac)
- [Vizio-supplied Linux and U-Boot sources for older MediaTek TV chips](https://github.com/unitedcolorsofg/vizio_oss)
- [ViziOwn research on SmartCast runtime configuration](https://bh2017.exploitee.rs/2021/viziown-exploiting-vizio-smartcast/)
- [SmartCast web bundle and internal API research](https://github.com/vindeckyy/smartcast-backdoor)
