"""ATLAS Open Data reference documentation embedded as MCP resources and instructions."""

from __future__ import annotations

ATLAS_OPEN_DATA_GUIDE = """\
# ATLAS Open Data — Quick Reference

## Releases
ATLAS Open Data publishes datasets under named releases. Each release
targets a specific use case (education or research) and centre-of-mass energy:

| Release              | Description                                              |
|----------------------|----------------------------------------------------------|
| 2016e-8tev           | 2016 education release, 8 TeV pp collisions              |
| 2020e-13tev          | 2020 education release, 13 TeV pp collisions             |
| 2024r-pp             | 2024 research release, proton-proton collisions          |
| 2024r-hi             | 2024 research release, heavy-ion collisions              |
| 2025e-13tev-beta     | 2025 education beta release, 13 TeV pp collisions        |
| 2025r-evgen-13tev    | 2025 research event-generation release, 13 TeV           |
| 2025r-evgen-13p6tev  | 2025 research event-generation release, 13.6 TeV         |

## Datasets
Within a release, each Monte Carlo sample is identified by a numeric
**dataset number** (DSID), e.g. `301204`, and a human-readable
**physics_short** name, e.g. `Sh_2211_Zee_maxHTpTV2_BFilter`.

## Physics Short Name Convention

The physics_short packs as much information as possible about a sample
into 50-60 characters. Parts are separated by underscores.

### Part 1: Generator abbreviations (required, always first)
The first part lists the generator program(s) used to produce the sample.

| Abbreviation | Generator                                    |
|--------------|----------------------------------------------|
| Sh           | Sherpa                                       |
| Ph           | Powheg                                       |
| Py8          | Pythia8                                      |
| MG           | MadGraph (normally LO)                       |
| aMC          | aMC@NLO (aMcAtNlo when spelled out)          |
| H7           | Herwig7                                      |
| Ag           | Alpgen                                       |
| EG           | EvtGen                                       |
| PG           | ParticleGun                                  |
| HepMC        | Samples created from HepMC text files        |

Full names like "Sherpa" or "Pythia8" may also appear. When Tauola or
Photos are used, they are **not** indicated in the name.

### Part 2: Tune / PDF / Sherpa version
The second part normally describes the PDF set and/or non-perturbative
physics tune:

- **Tunes**: A14, AZ, AZNLO (Pythia8/Herwig7), H7UE (Herwig7)
- **Sherpa**: The second field is the Sherpa version number, e.g.
  `222` = 2.2.2, `2211` = 2.2.11, `2212` = 2.2.12
- **PDFs**: NNPDF30NNLO, NNPDF23LO, MSTW2008LO, CTEQ6L1, etc.
  The name encodes the family, release, and perturbative order.

### Remaining parts: Physics process (no strict rules)
Beyond the first two parts, conventions are flexible but aim for
readability:

**Process abbreviations:**
- `tchan` = t-channel, `schan` = s-channel
- `myy` = diphoton mass, `pty` = photon momentum
- `Zee` = Z→ee, `Zmumu` = Z→μμ, `Wenu` = W→eν, etc.

**Decay modes:**
- `incl` / `inc` = inclusive (SM branching fractions)
- `dil` = di-lepton (e.g. both W bosons decay leptonically)
- `nonallhad` = at least one lepton
- `allhad` = all-hadronic

**Production features:**
- `FxFx` = FxFx merging prescription
- `HT2bias` = biased in HT2 for better high-energy statistics
- `SW` / `withSW` = biasing done within the generator itself
- `DS` = diagram subtraction (single top interference correction)
- `DR` = diagram removal (single top interference correction)

**Filters (usually at the end):**
- `MET200` = 200 GeV MET filter
- `BFilter` = at least one b-quark in the matrix element
- `BVetoCFilter` = no b-quark, at least one c-quark
- `BVetoCVeto` = no b-quarks or c-quarks
- These three heavy-flavor filters should be combined for a complete
  background estimate.
- `maxHTpTV2` = filter on HT and pT of the vector boson

**Example**: `Sh_2211_Zee_maxHTpTV2_BFilter` means:
- Sherpa 2.2.11
- Z→ee process
- maxHTpTV2 phase-space filter
- b-quark filter applied

The job options (Python configuration used to generate the sample) are
always the definitive reference for interpreting physics_short names.

## Skims
Skims are pre-filtered subsets of events sharing a characteristic
(e.g. `exactly4lep`, `3lep`). Processing a skim saves time when the
analysis selection is more restrictive than the skim selection.
Use `noskim` (default) for the full, unfiltered dataset.

## Metadata Fields
Each dataset carries metadata such as:
- `dataset_number`, `physics_short`, `e_tag`
- `cross_section_pb`, `genFiltEff`, `kFactor`
- `nEvents`, `sumOfWeights`, `sumOfWeightsSquared`
- `process`, `generator`, `keywords`, `description`
- `CoMEnergy`, `GenEvents`, `GenTune`, `PDF`, `Release`, `Filters`
- `file_list` (URLs), `skims` (skim objects with their own `file_list`)

## Protocols
File URLs can be served in three protocols:
- `root` — XRootD streaming (default)
- `https` — Web-accessible via opendata.cern.ch
- `eos` — EOS POSIX mount path

## Keywords
Datasets are tagged with physics keywords (e.g. `top`, `higgs`, `dilepton`)
that can be used for search and filtering via `match_metadata`.

## Weights (Monte Carlo)
For event-generation releases, weight metadata lists the available
systematic variations and PDF sets per DSID.
"""

METADATA_FIELDS_REFERENCE = """\
# ATLAS Open Data Metadata Fields

These fields are available for each dataset in a release. The exact set
depends on the release; use `atlas_get_metadata_fields` to see what is
available for the currently active release.

## Core identification
- `dataset_number` — Numeric dataset ID (DSID)
- `physics_short` — Structured sample name encoding generator, tune/PDF,
  process, decay mode, and filters (see Physics Short Name Convention in
  the ATLAS Open Data Guide resource for decoding rules)
- `e_tag` — Event-generation tag (e.g. `e8514`)
- `release.name` — Name of the release this dataset belongs to

## Physics parameters
- `cross_section_pb` — Production cross-section in picobarns
- `genFiltEff` — Generator-level filter efficiency
- `kFactor` — Higher-order correction factor
- `nEvents` — Number of events in the dataset
- `sumOfWeights` — Sum of event weights
- `sumOfWeightsSquared` — Sum of squared event weights
- `CoMEnergy` — Centre-of-mass energy (e.g. `13TeV`)

## Generation details
- `process` — Physics process description
- `generator` — MC generator used (e.g. `Pythia8`, `Sherpa`)
- `keywords` — List of physics keywords for filtering
- `description` — Human-readable dataset description
- `GenEvents` — Number of generated events
- `GenTune` — Generator tune (e.g. `A14`, `AZ`, `AZNLO`, `H7UE`)
- `PDF` — PDF set used (e.g. `NNPDF30NNLO`, `CTEQ6L1`)
- `Release` — Software release
- `Filters` — Generator-level filters applied

## File access
- `file_list` — List of ROOT file URLs
- `skims` — List of skim objects, each with `skim_type` and `file_list`
- `job_path` — Internal job path
"""
