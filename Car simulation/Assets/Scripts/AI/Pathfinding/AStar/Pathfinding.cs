using System;
using System.Collections.Generic;
using UnityEngine;

public class Pathfinding : MonoBehaviour
{
    public Transform seeker,
        target;
    PathGrid grid;

    private void Awake()
    {
        grid = GetComponent<PathGrid>();
    }

    private void Start()
    {
        
        
    }

    private void Update()
    {
        FindPath(seeker.position, target.position);
    }

    void FindPath(Vector3 startPos, Vector3 targetPos)
    {
        // convert position to node
        Node startNode = grid.NodeFromWorldPoint(startPos);
        Node targetNode = grid.NodeFromWorldPoint(targetPos);

        // open set nodes to be evaluated
        List<Node> openSet = new List<Node>();
        // closed set nodes already evaluated
        HashSet<Node> closedSet = new HashSet<Node>();
        // Add start node to openset
        openSet.Add(startNode);
        
        // if count reaches 0 no path :(
        while (openSet.Count > 0)
        {
            // make first element in the open current node
            Node currentNode = openSet[0];
            // loop every element in the openset
            for (int i = 1; i < openSet.Count; i++)
            {
                // If there is better path in openset replace current node with neighbour 
                if (
                    openSet[i].fCost < currentNode.fCost
                    || openSet[i].fCost == currentNode.fCost && openSet[i].hCost < currentNode.hCost
                )
                {
                    currentNode = openSet[i];
                }
            }
            // Move current node to closed "Already processed"
            openSet.Remove(currentNode);
            closedSet.Add(currentNode);
            // if current is target we found path YIPPEE
            if (currentNode == targetNode)
            {
                RetracePath(startNode, targetNode);
                return;
            }
            //Check all neighbours of current node
            foreach (var neighbour in grid.GetNeighbours(currentNode))
            {
                // ignore if its unpassable
                if (!neighbour.walkable || closedSet.Contains(neighbour))
                {
                    continue;
                }
                // Calculate neighbours movement cost
                int newMovementCostToNeighbour =
                    currentNode.gCost + GetDistance(currentNode, neighbour);
                //  Check if neighbour gCost is lower than currentNode neighbour distance (fCost)
                if (newMovementCostToNeighbour < neighbour.gCost || !openSet.Contains(neighbour))
                {
                    //set neighbours gcost to newMovCost
                   // Calculate hCost to neughbour 
                    neighbour.gCost = newMovementCostToNeighbour;
                    neighbour.hCost = GetDistance(neighbour, targetNode);
                    neighbour.parent = currentNode;
                    // Add it to openset/ next iteration for cost check
                    if (!openSet.Contains(neighbour))
                    {
                        openSet.Add(neighbour);
                    }
                }
            }
        }
        // Bad things happens 
        Debug.Log("Did not find path");
    }

    void RetracePath(Node startNode, Node endNode)
    {
        List<Node> path = new List<Node>();
        Node currentNode = endNode;
        while (currentNode != startNode)
        {
            path.Add(currentNode);
            currentNode = currentNode.parent;
        }
        path.Reverse();
        Debug.Log("found path");
        grid.path = path;
    }

    int GetDistance(Node a, Node b)
    {
        int dstX = Mathf.Abs(a.gridX - b.gridX);
        int dstY = Mathf.Abs(a.gridY - b.gridY);

        if (dstX > dstY)
        {
            return 14 * dstY + 10 * (dstX - dstY);
        }
        return 14 * dstX + 10 * (dstY - dstX);
    }
}
