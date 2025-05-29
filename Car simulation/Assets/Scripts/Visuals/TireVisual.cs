using UnityEngine;

public class TireVisual : MonoBehaviour
{
    [SerializeField] private Transform[] visuals;
    [SerializeField] private WheelCollider[] wheels;
    private Vector3 position;
    private Quaternion rotation;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        for (int i = 0; i < wheels.Length; i++)
        {
            wheels[i].GetWorldPose(out position, out rotation);
            visuals[i].position = position;
            visuals[i].rotation = rotation;
        }
        
    }
}
