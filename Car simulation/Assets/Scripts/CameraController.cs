using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private float distance;
    [SerializeField] private float sensitivity;

    private InputManager inputManager;
    private Vector2 cameraInput = new Vector2();
    
    private void Start()
    {
        inputManager = InputManager.Instance;
        
    }

    private void Update()
    {

        cameraInput = inputManager.GetNormalizedCarInput();
        Debug.Log(cameraInput);
        transform.position = target.position - transform.forward * distance; ;
        transform.rotation = Quaternion.Euler(new Vector3(0, 180, 0));
        
    }
}
