using UnityEngine;

public class HybridGrid : MonoBehaviour
{

    [SerializeField]
    private LayerMask unwalkableMask;

    [SerializeField]
    public Vector2 gridWorldSize;

    [SerializeField]
    public float cellRadius;

    public Cell[,] cells;
    float nodeDiameter;
    int gridSizeX,
        gridSizeY;
    void Start()
    {
       CreateGrid(); 
    }

    public void CreateGrid()
    {
        nodeDiameter = cellRadius* 2;
        gridSizeX = Mathf.RoundToInt(gridWorldSize.x / nodeDiameter);
        gridSizeY = Mathf.RoundToInt(gridWorldSize.y / nodeDiameter);
        cells = new Cell[gridSizeX, gridSizeY];
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
                    + Vector3.right * (x * nodeDiameter + cellRadius)
                    + Vector3.forward * (y * nodeDiameter + cellRadius);
                bool walkable = !(Physics.CheckSphere(worldPoint, cellRadius, unwalkableMask));
                cells[x, y] = new Cell(worldPoint,walkable);
            }
        }
    }
    
    public Cell CellFromWorldPoint(Vector3 worldPoint)
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
        return cells[x, y];
    }

    public bool IsPositionInGrid(Vector3 worldPoint)
    {
        float percentX =
            (worldPoint.x - (transform.position.x - gridWorldSize.x / 2)) / gridWorldSize.x;
        float percentY =
            (worldPoint.z - (transform.position.z - gridWorldSize.y / 2)) / gridWorldSize.y;
        return percentX >= 0 && percentX <= 1 && percentY >= 0 && percentY <= 1;
    }
    void OnDrawGizmos()
    {
        Gizmos.DrawWireCube(transform.position, new Vector3(gridWorldSize.x, 1, gridWorldSize.y));
        if (cells!= null)
        {
            foreach (var cell in cells)
            {
                Gizmos.color = (cell.isTravelsable) ? Color.white : Color.red;
                Gizmos.DrawCube(cell.centerPos, Vector3.one * (float)(nodeDiameter - 0.1));
            }
        }
    }
}
