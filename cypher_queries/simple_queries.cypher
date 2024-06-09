// count the number of Acitivities in the graph (operation performed in the pipeline)
MATCH (n:Activity) RETURN count(n);

//determination of the number of distinct activities performed and provides
a list of the activity names.
MATCH (n:Activity)
RETURN COUNT(DISTINCT n.function_name) AS activityNumber,
COLLECT(DISTINCT n.function_name) AS distinctActivities;

//retrieve all associated activities that have used this node
MATCH (e : Entity {id : `entity:ed7ff4dd-b198-4c55-88af-
f711e8b04695`})<-[:USED]-(a:Activity) RETURN collect(a);