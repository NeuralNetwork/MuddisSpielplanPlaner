%module example
    %{
    /* Includes the header in the wrapper code */
    #include "RankingGenerator.h"
    %}

    /* Parse the header file to generate wrappers */
    %include "RankingGenerator.h"