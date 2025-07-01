using UnityEngine;

public class HybridNode : IHeapItem<HybridNode>
{
    public float gCost;
    public float hCost;
    public float fCost { get { return gCost + hCost; } }
    
    
    public Vector3 frontWheelPos;
    public Vector3 backWheelPos;
    public float heading;
    public bool isReversing;

    public HybridNode previous;

    private int heapIndex;

    public HybridNode()
    {
        
    }

    public HybridNode(HybridNode previous,Vector3 backWheelPos, float heading, bool isReversing)
    {
        this.previous = previous;
        this.backWheelPos = backWheelPos;
        this.heading = heading;
        this.isReversing = isReversing;
        
    }
    public void AddCosts(float g, float h)
    {
        gCost = g;
        hCost = h;

    }
    public int HeapIndex
    {
        get
        {
            return heapIndex;
        }
        set
        {
            heapIndex = value;
        }
    }

    public int CompareTo(HybridNode other)
    {
        int compare = fCost.CompareTo(other.fCost);

        //If they are equal, use the one that is the closest
        //Will return 1, 0 or -1, so 0 means the f costs are the same
        if (compare == 0)
        {
            compare = hCost.CompareTo(other.hCost);
        }

        return -compare;
    }

}
