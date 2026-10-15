# Guía — Nodexys Kernel Builder

## 1. Compilar
1. **Actions** → **Nodexys Kernel Builder** → **Run workflow**.
2. Elige opciones y pulsa el botón verde.
3. Espera (30–90 min; con la caché es más rápido la segunda vez).
4. Abajo en la página del run: descarga **`<nombre>-<root>-5.10.<n>-clang<12|19>-AnyKernel3`**. Ya es un zip flasheable.
5. Si usaste NoMount, descarga también **NoMount-Metamodule** e instálalo desde tu manager de root.

Con `All` salen **dos** kernels (uno por cada clang): prueba primero el que prefieras; si uno no arranca, prueba el otro.

## 2. Cada opción
**[1 Fuente] `source_branch`** — La rama de `Nodexys/Kernel-Source`. Vacío usa la principal.

**[2 Compilador] `clang`** — Clang 19 (más nuevo), Clang 12 (más parecido al que usó Google para android12-5.10), o los dos. `lto`: `Del defconfig` no cambia nada; `thin` compila más rápido; `full` optimiza más pero tarda y usa mucha memoria; `ninguno` apaga LTO (y con ello CFI).

**[3 Root]** `KernelSU-Next` o `Sin root (vanilla)`. `SUSFS` solo funciona con KernelSU-Next. `NoMount` agrega el soporte en el kernel y genera su metamódulo.

**[4 Extras]** — `NTSync` (Wine/Proton), `Networking` (BBRv3, IPSet, CIFS, WireGuard…), `Rendimiento` (experimental, apagado por defecto), `DroidSpaces` (contenedores Linux), `Baseband Guard`, `BPF`, y dos parches de arreglo para SUSFS (`Ptrace` y `Unicode`). Si algo falla, apaga extras para encontrar al culpable.

**[5 KMI] `kmi_validation`** — Los módulos del vendor (WiFi, GPU…) se compilaron contra una versión concreta del kernel. 
- **ON (normal):** si los símbolos de un módulo no coinciden con los del kernel, el kernel lo rechaza.
- **OFF:** el kernel lo carga igual y solo avisa en `dmesg` (`disagrees about version of symbol ..., but ignore...`). Úsalo si tus módulos fallan por eso. Ojo: si las estructuras internas cambiaron de verdad, cargar el módulo puede causar cuelgues. Si la fuente ya trae ese comportamiento, el workflow lo detecta y no lo repite.

**[6 Nombre]** `brand_name` aparece en el nombre del zip y en el banner. `uname_suffix` cambia lo que muestra `uname -r`; vacío deja la versión del defconfig.

**[7 Configs]** `extra_configs`: `CONFIG_FOO=y CONFIG_BAR=n` (separadas por espacio). Se suman a `custom.config`.

**[8 Avanzado]** `extra_make_args` (ej: `KCFLAGS=-Wno-error`), `commit_mode` (`verified` = versiones probadas de NoMount; `latest` = lo más nuevo) y `use_cache`.

**[9 Salida]** `create_release` publica el zip en **Releases**.

## 3. Tus configs (`custom.config`)
Una config por línea (`CONFIG_FOO=y`, `CONFIG_FOO=n`, `# CONFIG_FOO is not set`…). Se aplican **al final** sobre `gki_defconfig`, así que ganan sobre todo. Al terminar, el resumen del run te avisa si alguna no quedó como la pediste (por ejemplo, por una dependencia).

## 4. Para el futuro
- **`patches/custom/`**: tus parches `.patch`, en orden alfabético, justo antes de compilar.
- **`hooks/pre-build.sh`**: un script que corre justo antes de compilar, dentro de la carpeta del kernel.
- **`anykernel/`**: `banner` (lo que se ve al flashear) y `anykernel.sh` (el instalador). Marcadores: `@BRAND@ @KVER@ @ROOT@ @FEATURES@ @DATE@`.

## 5. Dependencias externas
| Qué | De dónde | Dónde cambiarlo |
|---|---|---|
| El kernel | `Nodexys/Kernel-Source` | `KERNEL_SOURCE_REPO` en `build.yml` |
| Parches extra (ntsync, bbrv3…) | `WildKernels/kernel_patches` | `KERNEL_PATCHES_REPO` |
| Base de AnyKernel3 | `osm0sis/AnyKernel3` | `AK3_REPO` / `AK3_BRANCH` |
| Clang 12 | repos de Ubuntu 22.04 | — |
| Clang 19 | `apt.llvm.org` | — |

## 6. Si falla el build
- Mira el paso en rojo y busca `error:` con **Search logs**. Si el error final es solo `Error 2`, el verdadero está más arriba.
- Prueba con el otro clang (`All` ayuda).
- Los parches que no aplican se suben como artifact `...-Rejects`.

## 7. Si el teléfono no arranca (bootloop)
Restaura tu `boot` respaldado con `fastboot flash boot boot-respaldo.img`. Para investigar, copia `/sys/fs/pstore/` en el **primer** arranque después del fallo (el siguiente arranque lo sobrescribe).
