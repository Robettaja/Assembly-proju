using System.Collections.Generic;
using UnityEngine;

public class CarController : MonoBehaviour
{
    [SerializeField] private float speed;
    [SerializeField] private float rotationAmount;
    [SerializeField] private float forwardVelKMH;
    
    private Vector2 carInputs;
    private Rigidbody rb;
    private WheelCollider[] wheels;
    private InputManager inputManager;
    private void Start()
    {
        inputManager = InputManager.Instance;
        inputManager.OnCarFlip += InputManagerOnCarFlip;
        rb = GetComponent<Rigidbody>();
        wheels = GetComponentsInChildren<WheelCollider>();
    }

    private void InputManagerOnCarFlip()
    {
        transform.rotation = Quaternion.Euler(Vector3.zero);
    }

    private void FixedUpdate()
    {
        carInputs = inputManager.GetNormalizedCarInput();
        for(int i=0; i < wheels.Length; i++)
        {
            if (carInputs.magnitude != 0) ;
            wheels[i].brakeTorque = 0;
            // if (i >= 2 && i <= 3)
            {
                wheels[i].motorTorque = speed * carInputs.y;
            }
            if (i >= 0 && i <= 1)
            {
                wheels[i].steerAngle = rotationAmount * carInputs.x;
            }
            
        }
        forwardVelKMH = Vector3.Dot(transform.forward,rb.linearVelocity) * 3.6f;

    }
}
