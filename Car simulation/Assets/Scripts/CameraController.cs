using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private float distance;
    [SerializeField] private float sensitivity;

    private InputManager inputManager;
    private Vector2 cameraInput;

    private float yaw = 0f;
    private float pitch = 0f;
    
    private void Start()
    {
        inputManager = InputManager.Instance;
    }

    private void Update()
    { 
        cameraInput = inputManager.GetNormalizedCameraInput();
        
        yaw += cameraInput.x * sensitivity; 
        pitch -= cameraInput.y * sensitivity;
        pitch = Mathf.Clamp(pitch, -90, 90);
       
        Quaternion rotation = Quaternion.Euler(pitch, yaw, 0);
        Vector3 position = target.position - transform.forward * distance;
        
        transform.rotation = rotation;
        transform.localPosition = position;
        
        
    }
}
