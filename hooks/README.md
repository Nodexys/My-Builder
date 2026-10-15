# hooks

Si creas `hooks/pre-build.sh`, el workflow lo ejecuta justo antes de compilar, con la carpeta del kernel
como directorio actual (también en la variable `$KERNEL_DIR`). Sirve para cualquier ajuste que no sea un
parche ni una config: borrar un archivo, un `sed`, copiar algo, etc. Si el script falla, el build se detiene.
