using UnityEngine;

public class Node 
{
    /**Can you move to node */
    public bool walkable;
    /** Node position in world*/
    public Vector3 worldPos;
    public int gridX;
    public int gridY;

    /**Distance to the start node */
    public int gCost;
    
    /**Distance to the end node */
    public int hCost;
    public Node parent;
    
    /**Total distance (g + h costs). If duplicate determine with hCost */
    public int fCost { get { return gCost + hCost; }  }
    
    public Node(bool _walkable,Vector3 _worldPos,int _gridX, int _gridY) {
        walkable = _walkable;
        worldPos = _worldPos;
        gridX = _gridX;
        gridY = _gridY;
        
        }
}
