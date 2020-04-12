using UnityEngine;
using UnityEngine.UI;

public class screen_text : MonoBehaviour
{


    public Text sentence;

    // Update is called once per frame
    void Update()
    {
        sentence.text = "Hello World!";
    }
}
