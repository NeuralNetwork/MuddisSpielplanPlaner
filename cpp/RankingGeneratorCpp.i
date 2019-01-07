%module RankingGeneratorCpp
    %{
    /* Includes the header in the wrapper code */
    #include "RankingGenerator.h"
    %}

%include "std_vector.i";
namespace std {
  %template(vector_TeamInt) vector<TeamInt>;
  %template(vector_GameInt) vector<GameInt>;
}

/* Parse the header file to generate wrappers */
%include "RankingGenerator.h"

