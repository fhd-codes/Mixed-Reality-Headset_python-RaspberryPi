using UnityEngine;
using UnityEngine.UI;
using System.IO.Ports;

public class screen_text : MonoBehaviour
{

    SerialPort stream = new SerialPort("COM3", 9600);
    public Text sentence;

    void Start()
    {
        stream.Open(); //Open the Serial Stream.
    }
    // Update is called once per frame
    void Update()
    {
        string value = stream.ReadLine();
        sentence.text = value;

        //sentence.text = "Hello World!";
    }
}
