using UnityEngine;

public class RSCar  
{
    public enum Steering { Left, Right, Straight }
    public enum Gear { Forward, Back }

    public RSCar.Steering steering;
    public RSCar.Gear gear;
    public Vector3 pos;

    private float heading;

    public RSCar(Vector3 pos, float headingInRadians)
    {
        this.pos = pos;
        // this.heading = ReedsSheppPaths.PathLengthMath.M(headingInRadians);
    }
}
