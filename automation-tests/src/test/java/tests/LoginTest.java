package tests;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.Test;

public class LoginTest {

    WebDriver driver;

    @Test
    public void verifyGoogleTitle() {
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();

        driver.get("https://www.google.com");
        String title = driver.getTitle();

        Assert.assertTrue(title.contains("Google"),
                "Title validation failed");
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
