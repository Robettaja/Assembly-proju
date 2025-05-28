using UnityEngine;

public class WheelManager : MonoBehaviour
{
    [SerializeField] private bool update;
    [Header("General Settings")]
    public float radius = 0.35f;
    public float wheelMass = 20f;
    public float wheelDampingRate = 0.25f;
    public float suspensionDistance = 0.2f;

    [Header("Suspension Settings")]
    public float suspensionSpring = 35000f;
    public float suspensionDamper = 4500f;
    public float suspensionTargetPosition = 0.5f;

    [Header("Forward Friction")]
    public float forwardExtremumSlip = 0.4f;
    public float forwardExtremumValue = 1f;
    public float forwardAsymptoteSlip = 0.8f;
    public float forwardAsymptoteValue = 0.5f;
    public float forwardStiffness = 1f;

    [Header("Sideways Friction")]
    public float sidewaysExtremumSlip = 0.2f;
    public float sidewaysExtremumValue = 1f;
    public float sidewaysAsymptoteSlip = 0.5f;
    public float sidewaysAsymptoteValue = 0.75f;
    public float sidewaysStiffness = 1f;

    private WheelCollider[] wheels;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        wheels = GetComponentsInChildren<WheelCollider>();
        ApplySettings();
        
    }

    // Update is called once per frame
    void Update()
    {
        if (update)
        {
            ApplySettings();
        }
        
    } public void ApplySettings()
    {
        foreach (var wheel in wheels)
        {
            wheel.radius = radius;
            wheel.mass = wheelMass;
            wheel.wheelDampingRate = wheelDampingRate;
            wheel.suspensionDistance = suspensionDistance;

            JointSpring spring = wheel.suspensionSpring;
            spring.spring = suspensionSpring;
            spring.damper = suspensionDamper;
            spring.targetPosition = suspensionTargetPosition;
            wheel.suspensionSpring = spring;

            WheelFrictionCurve forward = wheel.forwardFriction;
            forward.extremumSlip = forwardExtremumSlip;
            forward.extremumValue = forwardExtremumValue;
            forward.asymptoteSlip = forwardAsymptoteSlip;
            forward.asymptoteValue = forwardAsymptoteValue;
            forward.stiffness = forwardStiffness;
            wheel.forwardFriction = forward;

            WheelFrictionCurve sideways = wheel.sidewaysFriction;
            sideways.extremumSlip = sidewaysExtremumSlip;
            sideways.extremumValue = sidewaysExtremumValue;
            sideways.asymptoteSlip = sidewaysAsymptoteSlip;
            sideways.asymptoteValue = sidewaysAsymptoteValue;
            sideways.stiffness = sidewaysStiffness;
            wheel.sidewaysFriction = sideways;
            
        }
    }
}
