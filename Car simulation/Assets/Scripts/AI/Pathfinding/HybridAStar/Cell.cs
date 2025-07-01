using UnityEngine;

public class Cell
{
    public Vector3 centerPos;
    public float heuristics;
    public bool isTravelsable;

    public Cell(Vector3 centerPos,bool isTravelsable)
    {
        this.centerPos = centerPos;
        this.isTravelsable = isTravelsable;

        heuristics = float.MaxValue;

    }
}
