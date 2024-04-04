# jq
[ 
    .curriculum.experiences[]? 
    | with_entries(select(.value | . != null))
    | .. | select(type == "object")
    | select( .typeExperience == "group" )
    | select( .typeExperience == "group" )
] 
