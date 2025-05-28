using System;
using UnityEngine;
using UnityEngine.InputSystem;

public class InputManager : MonoBehaviour,  InputSystem_Actions.ICarActions, InputSystem_Actions.ICameraActions
{
    public InputSystem_Actions inputAction; 
    
    private Vector2 carInput = Vector2.zero;
    private Vector2 cameraInput= Vector2.zero;
    public static InputManager Instance;


    private void Awake()
    {
        Instance = this;

        inputAction = new InputSystem_Actions();
        inputAction.Car.SetCallbacks(this);
        inputAction.Camera.SetCallbacks(this);

        inputAction.Car.Enable();
        inputAction.Camera.Enable();
    }

    public void OnMove(InputAction.CallbackContext context)
    {
        carInput = context.ReadValue<Vector2>();
    }
    public void OnCamMove(InputAction.CallbackContext context)
    {
        cameraInput = context.ReadValue<Vector2>();
    }

    public Vector2 GetNormalizedCarInput()
    {
        return carInput.normalized;
    }

    public Vector2 GetNormalizedCameraInput()
    {
       return cameraInput.normalized; 
    }

}
