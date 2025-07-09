using UnityEngine;

public static class CarSimulator  
{
    public static Vector3 CalculateNewPos(float theta, float beta, float d, Vector3 backWheelPos)
    {
        Vector3 newBackWheelPos= Vector3.zero;

        if (Mathf.Abs(theta) < 0.0001f)
        {
          newBackWheelPos.x  = backWheelPos.x + d * Mathf.Sin(theta);
          newBackWheelPos.z  = backWheelPos.z + d * Mathf.Cos(theta);   
        }
        else
        {
            float R = d / beta;
            float cx = backWheelPos.x + R * Mathf.Sin(theta);
            float cz = backWheelPos.z - R * Mathf.Cos(theta);
            
            newBackWheelPos.x = cx - R * Mathf.Sin(beta);
            newBackWheelPos.z = cz + R * Mathf.Cos(beta);
            
        }
        return newBackWheelPos;

    }

    public static float CalculateNewHeading(float theta, float beta)
    {
        theta = theta + beta;
        float PI = Mathf.PI;
        float TWO_PI = PI * 2f;
        
        theta= (float)System.Math.IEEERemainder((double)theta, (double)TWO_PI);


        if (theta> 2f * PI)
        {
            theta= theta - 2f * PI;
        }
        if (theta < 0f)
        {
            theta = 2f * PI + theta;
        }

        return theta;

    }
}
