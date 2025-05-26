using System.Collections.Generic;
using UnityEngine;

public class WheelManager : MonoBehaviour
{
    
    [SerializeField] private float mass;
    [SerializeField] private float spring;
    [SerializeField] private float damper;

    private List<WheelCollider> wheels = new List<WheelCollider>(); 
    private void Awake()
    {
        for (int i = 0; i < transform.childCount; i++)
        {
            wheels.Add(transform.GetChild(i).GetComponent<WheelCollider>());           
        }
    }

    private void Update()
    {
        foreach (WheelCollider wheel in wheels)
        {
            wheel.mass = mass;
            JointSpring jointSpring = wheel.suspensionSpring;
            jointSpring.spring = spring;
            jointSpring.damper = damper;
            wheel.suspensionSpring = jointSpring;
        }
        
    }

    public List<WheelCollider> GetWheels()
    {
        return wheels;
        
    }
}
