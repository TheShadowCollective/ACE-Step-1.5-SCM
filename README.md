# ACE-Step SCM 1.6

### The Muser's maintained ACE-Step compatibility fork

> [!IMPORTANT]
> **ACE-Step SCM is not a standalone Shadow Collective music-generation project.**
>
> This repository is a maintained fork of the original
> [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) project, created
> specifically to provide a compatible and reliable ACE-Step backend for
> **The Muser SCM**.
>
> Users of **The Muser SCM** should not need to install this repository directly.
> The Muser SCM's installation and startup system downloads, configures, and
> manages the compatible ACE-Step SCM environment automatically.


## Upstream Credit

**ACE-Step was created by the ACE-Step team and is co-led by ACE Studio and StepFun.**

The original ACE-Step project, model architecture, research, models, and
core implementation belong to their respective original authors and
contributors. The Shadow Collective did not create ACE-Step.

Original project:

**https://github.com/ace-step/ACE-Step-1.5**

Original ACE-Step 1.5 research citation:

> Junmin Gong, Yulin Song, Wenxiao Zhao, Sen Wang, Shengyuan Xu, and Jing Guo.
> *ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation* (2026).

ACE-Step SCM is forked on this repository because The Muser SCM depends on ACE-Step
and requires a known, tested version that can evolve alongside The Muser SCM's runtime
and integration requirements.

The Shadow Collective's work in this repository is focused on compatibility,
integration, environment management, and maintenance required by The Muser SCM.


## Relationship to The Muser SCM

ACE-Step SCM is a backend dependency of **The Muser SCM**.

The Muser SCM provides the user-facing installation and orchestration workflow.
During first-time setup, `Start_Muser.bat` obtains and prepares the compatible
ACE-Step SCM version required for music generation.

Users installing The Muser SCM therefore should **not clone or configure
ACE-Step SCM separately**. Its environment, dependencies, models, compatibility
patches, and API startup are managed as part of The Muser SCM workflow.

The normal relationship is:

```text
The Muser SCM
    |
    | installs and manages
    v
ACE-Step SCM
    |
    | provides the music-generation backend
    v
ACE-Step models
```

This repository remains available separately so that the ACE-Step SCM integration
required by The Muser SCM can be developed, tested, versioned, and maintained
without modifying or depending upon the release schedule of the original
ACE-Step project.


## SCM Modernization

ACE-Step SCM preserves the original ACE-Step architecture while maintaining
the compatibility layer required by The Muser SCM.

The current SCM environment has been modernized and validated with:

- **Python 3.14**
- **PyTorch 2.13.0 + CUDA 13.0**
- **Transformers 5.x**
- **torchao 0.18.0**
- **vector-quantize-pytorch 1.31.1**
- **accelerate 1.14.0**
- **safetensors 0.8.0**

Additional SCM compatibility work includes:

- TorchAO PyTree enum compatibility
- `vector-quantize-pytorch` meta-device compatibility
- `pytorch-wavelets` modern `importlib.resources` compatibility
- Dedicated SCM environment bootstrap and validation
- ACE-Step REST API startup for The Muser SCM integration
- GPU detection and hardware-aware model selection

These changes are maintained specifically for the validated SCM workflow.
They should not be interpreted as replacements for the broader platform
support, installation methods, or development direction of the original
ACE-Step project.

## Why This Fork Exists

The Shadow Collective's SCM projects are being developed in support of a
personal AI-assisted fan-fiction art project.

The software work in this repository grew out of practical production needs.
When the existing software stack could not provide the environment,
compatibility, integration, or workflow required by the project, we modified
it so that the creative work could continue.

Those modifications are shared publicly in the hope that they may also be
useful to others, but **ACE-Step SCM is not intended to replace the original
ACE-Step project or redefine its supported platforms and workflows**.

Our development priority is the hardware and software environment used for
The Shadow Collective's own production work. We test ACE-Step SCM as part of
The Muser SCM workflow on our own hardware and make no guarantee that SCM
changes will behave as the original ACE-Step developers intended on other
hardware, operating systems, configurations, or workflows.

Where possible, SCM changes are kept isolated from the original ACE-Step
architecture so that upstream functionality is disturbed as little as
possible.

For general-purpose ACE-Step installation, platform support, documentation,
and development, users should refer to the original ACE-Step project:

https://github.com/ace-step/ACE-Step-1.5


## Validated Environment

ACE-Step SCM is developed and tested as part of The Muser SCM workflow on
The Shadow Collective's production hardware.

Current validated configuration:

- **Operating system:** Windows
- **GPU:** NVIDIA GeForce RTX 5060 Ti
- **VRAM:** 16 GB
- **CUDA:** 13.0
- **Python:** 3.14
- **PyTorch:** 2.13.0 + cu130

For The Muser SCM workflow, we recommend an **NVIDIA GPU with 16 GB of VRAM
or more**.

This is a recommendation based on the hardware used to develop and validate
the SCM integration. It is **not a statement of the minimum hardware
requirements of the original ACE-Step project**.

Other GPUs, VRAM capacities, operating systems, and hardware backends may
work, particularly where they are supported by upstream ACE-Step, but they
have not been validated by The Shadow Collective for the SCM workflow.

The Shadow Collective cannot guarantee compatibility or provide equivalent
validation for hardware and software configurations that we do not have
available for testing.


## For The Muser SCM Users

If you are using **The Muser SCM**, you do not need to install ACE-Step SCM
manually.

Install and start The Muser SCM using its normal startup workflow:

```bat
Start_Muser.bat
```

The Muser SCM will automatically:

- Detect whether the required ACE-Step SCM installation is present
- Download the compatible ACE-Step SCM repository when required
- Create and prepare its dedicated SCM Python environment
- Install the validated dependencies and compatibility patches
- Detect the available GPU configuration
- Select the appropriate ACE-Step model configuration
- Start the ACE-Step SCM REST API when required

ACE-Step SCM is intentionally maintained as a managed dependency so that
users of The Muser SCM do not need to maintain a separate ACE-Step
installation or reproduce its compatibility environment themselves.

If ACE-Step SCM is already installed and ready, The Muser SCM reuses the
existing installation rather than rebuilding it during every startup.


### Storage Requirements

A complete **The Muser SCM** installation requires substantial disk space.

During fresh-installation testing, the complete working environment occupied
approximately **43 GB** once The Muser SCM, ACE-Step SCM, Ollama, the
orchestration model, Python environments, dependencies, and generation models
were installed.

We recommend having at least **60 GB of free disk space** before beginning a
new The Muser SCM installation.

The additional space provides room for installation overhead, package and
model updates, temporary files, and generated music.

> [!IMPORTANT]
> The approximately 43 GB figure is a measured result from our validated
> installation, not a guaranteed fixed installation size. Actual disk usage
> may vary as dependencies, models, and upstream components change.


## For Developers

Direct installation and startup of ACE-Step SCM is intended primarily for
development, testing, and maintenance of The Muser SCM integration.

Normal users of The Muser SCM should use `Start_Muser.bat` instead.

### SCM Environment Setup

From the ACE-Step SCM repository root, the SCM environment can be prepared
with:

```bat
scripts\scm\bootstrap_scm_environment.bat
```

The bootstrap process creates the dedicated `.venv-scm` environment and
installs the dependencies and compatibility patches used by the
ACE-Step SCM environment.

> [!IMPORTANT]
> First-time setup may download several large dependencies and models.
> Make sure sufficient disk space is available before running the bootstrap
> process.

### Starting the SCM API

The ACE-Step SCM REST API used by The Muser SCM can be started directly with:

```bat
scripts\scm\start_api_server_scm.bat
```

The API listens on port `8001` by default.

When started through The Muser SCM, these environment and API-management
steps are handled automatically by The Muser SCM startup workflow.

### Development Scope

Changes to ACE-Step SCM should be made with The Muser SCM integration in mind.

When modifying the SCM environment, dependencies, compatibility patches,
hardware detection, model configuration, or API behavior, validate the
affected workflow through The Muser SCM whenever practical.

The broader ACE-Step project supports platforms and workflows beyond those
validated by The Shadow Collective. SCM-specific changes should avoid altering
unrelated upstream behavior unless a change is required for The Muser SCM 
integration.


## Upstream ACE-Step Documentation

ACE-Step SCM is maintained for integration with The Muser SCM and does not
attempt to duplicate the complete documentation of the original ACE-Step
project.

For standalone ACE-Step installation, supported platforms, model selection,
training, inference, user interfaces, API documentation, tutorials, and
general ACE-Step usage, please refer to the original project:

**ACE-Step 1.5:**  
https://github.com/ace-step/ACE-Step-1.5

The upstream documentation should be considered authoritative for original
ACE-Step functionality that has not been specifically modified or documented
by the SCM fork.

If behavior differs between ACE-Step SCM and the original ACE-Step project,
the SCM documentation applies only to the SCM-specific integration and
environment maintained for The Muser SCM.


## License & Attribution

ACE-Step SCM is derived from the original **ACE-Step 1.5** project and
continues to be distributed under the terms of the repository's
[MIT License](./LICENSE).

The original ACE-Step project, research, models, architecture, and core
implementation were created by the ACE-Step team and their contributors.
ACE-Step is co-led by **ACE Studio** and **StepFun**.

The Shadow Collective's contributions to this fork consist of modifications
made for compatibility, integration, environment management, and maintenance
required by The Muser SCM.

Nothing in the ACE-Step SCM name or documentation is intended to imply that
The Shadow Collective created the original ACE-Step project or is affiliated
with, endorsed by, or acting on behalf of the original ACE-Step developers.

Please preserve the original copyright, license, attribution, and third-party
notices when redistributing this software.

## Original ACE-Step Citation

If you use ACE-Step or ACE-Step SCM in research or other work where citation
is appropriate, please credit the original ACE-Step authors:

```bibtex
@misc{gong2026acestep,
    title={ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation},
    author={Junmin Gong, Yulin Song, Wenxiao Zhao, Sen Wang, Shengyuan Xu, Jing Guo},
    howpublished={\url{https://github.com/ace-step/ACE-Step-1.5}},
    year={2026},
    note={GitHub repository}
}
```

ACE-Step SCM would not exist without the work of the original ACE-Step
developers and contributors. We are grateful that their work was made
available to the open-source community.
