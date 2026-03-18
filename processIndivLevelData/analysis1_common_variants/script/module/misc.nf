process gather_file{
    label 'tiny'
    module 'R/4.3.0'
    publishDir "result", mode: 'copy', overwrite: true
    input:
        path(inputs)
        val(name)
    output:
        path("${name}")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    files <- list.files()
    res <- NULL
    for (i in files) {
        res %<>% rbind(., fread(i), fill = T)
    }
    fwrite(res, "${name}")
    """

}