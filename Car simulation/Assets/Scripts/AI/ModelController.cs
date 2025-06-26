using System;
using UnityEngine;

public class ModelController : MonoBehaviour
{
public Transform target;
    public float speed = 5f;              
    public float wheelbase = 2.5f;         
    public float maxSteeringAngle = 30f;    
    public float stoppingDistance = 0.5f;    

    private float steeringAngle = 0f;        

    void Update()
    {
        if (target == null) return;

        Vector3 direction = target.position - transform.position;
        float distance = direction.magnitude;

        if (distance < stoppingDistance)
        {
            return;
        }

        float desiredAngle = Mathf.Atan2(direction.z, direction.x) * Mathf.Rad2Deg;

        float currentAngle = transform.eulerAngles.y;

        float angleDiff = Mathf.DeltaAngle(currentAngle, desiredAngle);

        steeringAngle = Mathf.Clamp(angleDiff, -maxSteeringAngle, maxSteeringAngle);

        float delta = steeringAngle * Mathf.Deg2Rad;

        float dt = Time.deltaTime;
        float theta = currentAngle * Mathf.Deg2Rad;

        float x = transform.position.x + speed * Mathf.Cos(theta) * dt;
        float z = transform.position.z + speed * Mathf.Sin(theta) * dt;
        float thetaNew = theta + (speed / wheelbase) * Mathf.Tan(delta) * dt;

        transform.position = new Vector3(x, transform.position.y, z);
        transform.rotation = Quaternion.Euler(0f, thetaNew * Mathf.Rad2Deg, 0f);
    }

    }


