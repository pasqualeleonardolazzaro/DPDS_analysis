//Find the top-k longest path represents the entity that have been modified the mostin the pipeline

//New property to give a weight to edges
MATCH ()-[r:WAS_DERIVED_FROM]-()
SET r.newProperty = 1.0;
//Projection on WAS_DERIVED_FROM
CALL gds.graph.drop(`proj`, false);
CALL gds.graph.project(`proj`, [`Entity`],
{ WAS_DERIVED_FROM:{orientation:`NATURAL`, properties:`newProperty`} } );
//Query finding top-5 longest path
CALL gds.allShortestPaths.stream(
`proj`,
{relationshipWeightProperty: `newProperty`}
)
YIELD sourceNodeId, targetNodeId, distance
WITH sourceNodeId, targetNodeId, distance
RETURN sourceNodeId AS source, targetNodeId
AS target, distance
ORDER BY distance DESC
LIMIT 5;


//finding path of a given node by its ID

CALL gds.allShortestPaths.stream(
11
`proj`,
{relationshipWeightProperty: `newProperty`}
)
YIELD sourceNodeId, targetNodeId, distance
WITH sourceNodeId, targetNodeId, distance
WHERE sourceNodeId = 382
RETURN collect(targetNodeId) as pathNodes;