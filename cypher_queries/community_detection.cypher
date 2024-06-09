//2 projections:

//1)
CALL gds.graph.project(`proj`, [`Entity`],
{ WAS_DERIVED_FROM:{orientation:`NATURAL`} } );

//2)
CALL gds.graph.project(`proj`, [`Entity`],
{ WAS_DERIVED_FROM:{orientation:`NATURAL`},
USED:{orientation:`NATURAL`}, WAS_GENERATED_BY:
{orientation:`NATURAL`}} );

//Louvain
CALL gds.louvain.mutate(`proj`, {mutateProperty:`communityId`});
CALL gds.graph.nodeProperty.stream(`proj`,`communityId`, [`Entity`])
YIELD nodeId, propertyValue
WITH gds.util.asNode(nodeId) AS n, propertyValue AS communityId
WHERE n:Entity
RETURN n, communityId
ORDER BY communityId ASC;

//Core Decomposition
CALL gds.kcore.stream(`proj`)
YIELD nodeId, coreValue
RETURN gds.util.asNode(nodeId).id AS id, coreValue ORDER BY coreValue DESC;

//Weakly Connected Component method
CALL gds.wcc.stream(`proj`)
YIELD nodeId, componentId
RETURN gds.util.asNode(nodeId).id AS name, componentId
ORDER BY componentId, name;

//Eigenvector Centrality
CALL gds.eigenvector.stream(`proj`)
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS name, score
ORDER BY score DESC, name ASC;

//Betweeness Centrality
CALL gds.betweenness.stream(`proj`)
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS name, score
ORDER BY score DESC;