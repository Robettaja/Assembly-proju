using System.Collections.Generic;   
using UnityEngine;

public class CarController : MonoBehaviour
{
    [SerializeField] private WheelManager wheelManager;
    [SerializeField] private float speed;
    [SerializeField] private float rotationSpeed;
    private List<WheelCollider> wheels;
    
    private InputManager inputManager;
    private void Start()
    {
        wheels = wheelManager.GetWheels();
        inputManager = InputManager.Instance;
    }

    private void Update()
    {
        Vector2 carInputs = inputManager.GetNormalizedCarInput();
        wheels[0].steerAngle = wheels[1].steerAngle =  rotationSpeed * carInputs.x;
        wheels[0].motorTorque = wheels[1].motorTorque =  speed * carInputs.y;

    }
}
