package tests;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.Test;

public class SampleUITest {

    @Test
    public void verifyGoogleTitle() {
        WebDriver driver = new ChromeDriver();
        driver.get("https://www.google.com");

        // Intentional assertion for demo
        Assert.assertTrue(driver.getTitle().contains("Google"));

        driver.quit();
    }
}
