### AnyKernel3 Ramdisk Mod Script
## @BRAND@ Kernel - GKI android12-5.10
## Base: osm0sis @ xda-developers (AnyKernel3)
##
## Los textos @BRAND@, @KVER@, @ROOT@, @FEATURES@ y @DATE@ los rellena el workflow
## de GitHub Actions al compilar. El archivo "banner" (en esta misma carpeta) es el
## que se muestra al flashear: editalo si quieres cambiar el diseno.

### AnyKernel setup
# global properties
properties() { '
kernel.string=@BRAND@ Kernel @KVER@ (@ROOT@)
do.devicecheck=0
do.modules=0
do.systemless=0
do.cleanup=1
do.cleanuponabort=0
device.name1=
device.name2=
device.name3=
device.name4=
device.name5=
supported.versions=
supported.patchlevels=
supported.vendorpatchlevels=
'; } # end properties


### AnyKernel install
# GKI: el kernel va dentro de boot.img junto con un ramdisk genérico, no se toca nada más.
BLOCK=boot;
IS_SLOT_DEVICE=auto;
RAMDISK_COMPRESSION=auto;
PATCH_VBMETA_FLAG=auto;

# import functions/variables and setup patching - see for reference (DO NOT REMOVE)
. tools/ak3-core.sh;

ui_print " ";
ui_print "  Flasheando @BRAND@ Kernel @KVER@ ...";

# boot install (GKI: se reemplaza solo la imagen del kernel)
split_boot;
flash_boot;

ui_print " ";
ui_print "  Listo. Reinicia el telefono.";
## end install
