# patches/custom

Pon aquí cualquier parche `.patch` tuyo (formato `git diff` o `git format-patch`).
Se aplican sobre el kernel, en orden alfabético (`0001-...`, `0002-...`), **después** de todos los extras
(SUSFS, NTSync, etc.) y **antes** de compilar. Si uno falla, el build se detiene y dice cuál.
Carpeta vacía = no pasa nada.
