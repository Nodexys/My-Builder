<div align="center">

# Nodexys Kernel Builder

Compila el kernel de [Nodexys/Kernel-Source](https://github.com/Nodexys/Kernel-Source) con **KernelSU-Next + SUSFS** y extras, usando solo GitHub Actions. Todo se baja de GitHub.

</div>

> [!CAUTION]
> Flashear un kernel puede dejar el teléfono sin arrancar. Haz backup de la partición `boot` antes de flashear y úsalo bajo tu propio riesgo.

## Cómo compilar

1. Pestaña **Actions** → **Nodexys Kernel Builder** → **Run workflow**.
2. Elige opciones (las que no entiendas, déjalas como vienen).
3. Cuando termine, baja el artifact `...-AnyKernel3` al final de la página del run y flashéalo.

Guía completa, con cada opción explicada: **[docs/guia.md](docs/guia.md)**

## Opciones (en el orden del menú)

| Grupo | Opción | Qué hace |
|---|---|---|
| 1 Fuente | `source_branch` | Rama de tu repo del kernel (vacío = la principal) |
| 2 Compilador | `clang` | Clang 19, Clang 12, o **All** (compila con los dos y genera 2 kernels) |
| 2 Compilador | `lto` | `Del defconfig` (no tocar), `thin`, `full` o `ninguno` |
| 3 Root | `root` | KernelSU-Next o Sin root (vanilla) |
| 3 Root | `use_susfs` / `use_nomount` | SUSFS (oculta root) / NoMount + su metamódulo |
| 4 Extras | `use_ntsync` `use_net` `use_perf` `use_ds` `use_bbg` `use_bpf` `use_ptrace` `use_unicode` | Un check por extra |
| 5 KMI | `kmi_validation` | ON = normal. OFF = los módulos cargan aunque sus símbolos (CRC) no coincidan |
| 6 Nombre | `brand_name` / `uname_suffix` | Nombre del zip y banner / texto de `uname -r` |
| 7 Configs | `extra_configs` | Configs sueltas (se suman a `custom.config`) |
| 8 Avanzado | `extra_make_args` `commit_mode` `use_cache` | Para casos especiales |
| 9 Salida | `create_release` | Publica el zip en Releases |

## Personalízalo sin tocar el workflow

| Quiero... | Lo pongo en... |
|---|---|
| Cambiar/añadir configs del kernel | [`custom.config`](custom.config) (ganan sobre todo lo demás) |
| Aplicar un parche mío | [`patches/custom/`](patches/custom/) (archivos `.patch`) |
| Hacer algo raro antes de compilar | [`hooks/pre-build.sh`](hooks/) |
| Cambiar el banner o el instalador | [`anykernel/`](anykernel/) (`banner`, `anykernel.sh`) |

## Créditos

Basado en [WildKernels/GKI_KernelSU_SUSFS](https://github.com/WildKernels/GKI_KernelSU_SUSFS) (GPL-3.0). Ver [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
