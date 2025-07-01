using System;
using System.Collections.Generic;
using UnityEngine;

public class PathGrid : MonoBehaviour
{
    public List<Node> path;

    [SerializeField]
    private Transform player;

    [SerializeField]
    private LayerMask unwalkableMask;

    [SerializeField]
    private Vector2 gridWorldSize;

    [SerializeField]
    private float nodeRadius;

    Node[,] grid;
    float nodeDiameter;
    int gridSizeX,
        gridSizeY;

    private void Awake()
    {
        
        nodeDiameter = nodeRadius * 2;
        // Size of single grid
        gridSizeX = Mathf.RoundToInt(gridWorldSize.x / nodeDiameter);
        gridSizeY = Mathf.RoundToInt(gridWorldSize.y / nodeDiameter);
        CreateGrid();
    }

    private void Start()
    {
    }

    void CreateGrid()
    {
        grid = new Node[gridSizeX, gridSizeY];
        Vector3 worldBottomLeft =
            transform.position
            - Vector3.right * gridWorldSize.x / 2
            - Vector3.forward * gridWorldSize.y / 2;
        for (int x = 0; x < gridSizeX; x++)
        {
            for (int y = 0; y < gridSizeY; y++)
            {
                Vector3 worldPoint =
                    worldBottomLeft
                    + Vector3.right * (x * nodeDiameter + nodeRadius)
                    + Vector3.forward * (y * nodeDiameter + nodeRadius);
                bool walkable = !(Physics.CheckSphere(worldPoint, nodeRadius, unwalkableMask));
                grid[x, y] = new Node(walkable, worldPoint, x, y);
            }
        }
    }

    public List<Node> GetNeighbours(Node node)
    {
        
        List<Node> neighbours = new List<Node>();
        for (int x = -1; x <= 1; x++)
        {
            // loop through -1 to 1 relative indexes
            for (int y = -1; y <= 1; y++)
            {
                if (x == 0 && y == 0)
                {
                    continue;
                }
                // gets surrounding nodes from this node
                int checkX = node.gridX + x;
                int checkY = node.gridY + y;
                // check if node is out of bounds and within -1 to 1 range
                if (checkX >= 0 && checkX < gridSizeX && checkY >= 0 && checkY < gridSizeY)
                {
                    neighbours.Add(grid[checkX, checkY]);
                }
            }
        }
        return neighbours;
    }

    public Node NodeFromWorldPoint(Vector3 worldPoint)
    {
        // Uses percentage to convert worldpos to grid
        float percentX =
            (worldPoint.x - (transform.position.x - gridWorldSize.x / 2)) / gridWorldSize.x;
        float percentY =
            (worldPoint.z - (transform.position.z - gridWorldSize.y / 2)) / gridWorldSize.y;

        percentX = Mathf.Clamp01(percentX);
        percentY = Mathf.Clamp01(percentY);

        int x = Mathf.RoundToInt((gridSizeX - 1) * percentX);
        int y = Mathf.RoundToInt((gridSizeY - 1) * percentY);
        return grid[x, y];
    }

    //Visuals
    void OnDrawGizmos()
    {
        Gizmos.DrawWireCube(transform.position, new Vector3(gridWorldSize.x, 1, gridWorldSize.y));
        if (grid != null)
        {
            foreach (var node in grid)
            {
                Gizmos.color = (node.walkable) ? Color.white : Color.red;
                if (path != null)
                {
                    if (path.Contains(node))
                    {
                        Gizmos.color = Color.black;
                    }
                }
                Gizmos.DrawCube(node.worldPos, Vector3.one * (float)(nodeDiameter - 0.1));
            }
        }
    }
}
