using System.Collections.Generic;   
using UnityEngine;

public class CarController : MonoBehaviour
{
    [SerializeField] private WheelManager wheelManager;
    private List<WheelCollider> wheels;
    private void Start()
    {
        wheels = wheelManager.GetWheels();
    }

    private void Update()
    {
        wheels[0].motorTorque = wheels[1].motorTorque =  32;
        wheels[0].steerAngle = wheels[1].steerAngle =  0;

    }
}
