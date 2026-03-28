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
**physics_short** name, e.g. `zprime_ee`.

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
- `physics_short` — Short physics process name (e.g. `zprime_ee`)
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
- `GenTune` — Generator tune
- `PDF` — PDF set used
- `Release` — Software release
- `Filters` — Generator-level filters applied

## File access
- `file_list` — List of ROOT file URLs
- `skims` — List of skim objects, each with `skim_type` and `file_list`
- `job_path` — Internal job path
"""
