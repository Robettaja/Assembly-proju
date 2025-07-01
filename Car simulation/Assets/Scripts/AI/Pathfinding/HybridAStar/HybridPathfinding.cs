using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

public class HybridPathfinding : MonoBehaviour
{
    
    public HybridGrid grid;
    public float driveDistance; 
    public float[] driveDistances;

    public const float MAX_ANGLE = 30f;
    public float[] steeringAngles = new float[] {MAX_ANGLE * Mathf.Deg2Rad,0, -MAX_ANGLE * Mathf.Deg2Rad};

    public const float HEADING_RESOLUTION = 15f;
    public const float MIN_DISTANCE = 1f;
    public const float MIN_ROTATION = 10f;
    public const float MIN_REEDS_PATH_DIST = 10f;
    
    int nodeCount = 0;


    public List<HybridNode> FindPath(Vector3 start, Vector3 end)
    {
        int prunedNodes = 0;

        int mapWidth = (int)grid.gridWorldSize.x;
        Cell[,] cells = grid.cells;
        
        Heap<HybridNode> openSet = new Heap<HybridNode>(200000);
        HashSet<int> [,] closedSet = new HashSet<int>[mapWidth,mapWidth];
        Dictionary<int,HybridNode>[,] lowestCostNodes = new Dictionary<int,HybridNode>[mapWidth,mapWidth];
        for (int x = 0; x < mapWidth; x++)
        {
            for (int z = 0; z < mapWidth; z++)
            {
                closedSet[x,z] = new HashSet<int>();
                lowestCostNodes[x,z] = new Dictionary<int, HybridNode>();
            }
        }

        Cell startCell = grid.CellFromWorldPoint(start);
        HybridNode node = new HybridNode(
            previous: null,
            backWheelPos: start,
            heading: 69f,
            isReversing: false);
        node.AddCosts( 0f,cells[(int)startCell.centerPos.x,(int)startCell.centerPos.z].heuristics);;
        openSet.Add(node);
        HybridNode finalNode = null;
        
        bool found= false;
        bool resing = false;

        int iterations = 0;
        Cell goalCell = grid.CellFromWorldPoint(end);
        while (!found && !resing)
        {
            if (iterations > 500000)
            {
                Debug.Log("stuck in infinite loop");
                break;
            }
            iterations++;
            if (openSet.Count == 0)
            {
                Debug.Log("path not found");
            }
            else
            {
                if (openSet.Count > nodeCount)
                {
                    nodeCount = openSet.Count;
                }

                HybridNode nextNode = openSet.RemoveFirst();
                Cell cell = grid.CellFromWorldPoint(nextNode.backWheelPos);
                // round to nearest heading
                int roundedHeading = (int)(Mathf.Round(nextNode.heading * Mathf.Rad2Deg/ HEADING_RESOLUTION) * HEADING_RESOLUTION);
                HashSet<int> closedHeadingsInThisCell = closedSet[(int)cell.centerPos.x,(int)cell.centerPos.z];
                bool isCellClosed = false;
                if (!closedHeadingsInThisCell.Contains(roundedHeading))
                {
                   closedHeadingsInThisCell.Add(roundedHeading); 
                }
                else
                {
                    isCellClosed = true;
                }

                if (isCellClosed)
                {
                    iterations -= 1;
                    continue;
                }
                float distanceSqrToGoal = (nextNode.backWheelPos - end).sqrMagnitude;
                //TODO Get correct heading value pwease
                float headingDiff = Mathf.Abs(roundedHeading - nextNode.heading * Mathf.Rad2Deg);
                if (distanceSqrToGoal < MIN_DISTANCE * MIN_DISTANCE || ((int)cell.centerPos.x == (int)goalCell.centerPos.x && ((int)cell.centerPos.z == (int)goalCell.centerPos.z))&& headingDiff <MIN_ROTATION)
                {
                    found = true;
                    Debug.Log("path found");
                    finalNode = nextNode;
                    
                    //TODO add final node stuff
                }
                else
                {
                    
                }
                
                
            }
            
        }
        return null;
    }
    
    private void Start()
    {
        driveDistance = Mathf.Sqrt((grid.cellRadius * grid.cellRadius) * 2f + 0.01f);
        driveDistances = new float[]{driveDistance,-driveDistance} ;
    }
}
