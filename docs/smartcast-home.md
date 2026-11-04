# SmartCast Home research

The public app metadata catalog and chipset availability table are JSON. Their app IDs can be compared across the two feeds. The availability feed describes eligibility by chipset and firmware, while the metadata feed describes apps and their artwork. A separate configuration download is binary. Its relationship to Home tile storage still needs to be established.

| Layer | Evidence to collect |
| --- | --- |
| Catalog metadata | App ID, displayed name, and icon |
| Availability | Chipset and firmware eligibility for that ID |
| Home placement | Which local or service-backed state records a tile and its ordering |
| Launch | Which runtime and launch parameters the selected tile resolves to |

To investigate a tile, trace one existing catalog ID through these layers. An app that can be launched through the local API may still have no corresponding Home entry. Likewise, a modified Input menu entry only establishes a change to the Input menu. For a Home tile result, record the display name and icon, verify that selection launches the intended app, and check whether it remains after reboot.

## Public references

- [Vizio app metadata](https://scfs.vizio.com/appservice/vizio_apps_prod.json)
- [Vizio app availability](https://scfs.vizio.com/appservice/app_availability_prod.json)
- [Vizio binary configuration](https://scfs.vizio.com/config/sc-config.enc)
- [vizaio catalog handling](https://github.com/raman325/vizaio)
- [SmartCast launch API implementation](https://github.com/get-air/vizio)
- [ViziOwn Input menu research](https://bh2017.exploitee.rs/2021/viziown-exploiting-vizio-smartcast/)
