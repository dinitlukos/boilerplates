import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.GenericUrl;
import com.google.api.client.http.HttpRequest;
import com.google.api.client.http.HttpRequestFactory;
import com.google.api.client.http.HttpResponse;
import com.google.api.client.http.HttpContent;
import com.google.api.client.http.json.JsonHttpContent;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.gson.GsonFactory; // Using GsonFactory for JSON
import com.google.auth.http.HttpCredentialsAdapter;
import com.google.auth.oauth2.GoogleCredentials;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class CloudRunMultiRouteClient {

    // Replace with your Cloud Run base endpoint URL (e.g., https://my-service-xyz-uc.a.run.app)
    private static final String BASE_CLOUD_RUN_ENDPOINT = "YOUR_CLOUD_RUN_BASE_URL";

    // Initialize JSON Factory (e.g., for request bodies)
    private static final JsonFactory JSON_FACTORY = GsonFactory.getDefaultInstance();

    public static void main(String[] args) {
        try {
            // Use Application Default Credentials for authentication
            GoogleCredentials credentials = GoogleCredentials.getApplicationDefault();
            HttpRequestFactory requestFactory = GoogleNetHttpTransport.newTrustedTransport()
                    .createRequestFactory(new HttpCredentialsAdapter(credentials));

            // --- Access Route 1: GET all items ---
            System.out.println("--- Accessing GET /data/items ---");
            String allItemsResponse = sendGetRequest(requestFactory, BASE_CLOUD_RUN_ENDPOINT + "/data/items");
            System.out.println("Response for /data/items: " + allItemsResponse);
            System.out.println("----------------------------------\n");

            // --- Access Route 2: GET a specific item (e.g., item with ID "123") ---
            System.out.println("--- Accessing GET /data/item/123 ---");
            String specificItemResponse = sendGetRequest(requestFactory, BASE_CLOUD_RUN_ENDPOINT + "/data/item/123");
            System.out.println("Response for /data/item/123: " + specificItemResponse);
            System.out.println("-------------------------------------\n");

            // --- Access Route 3: POST to create a new item ---
            System.out.println("--- Accessing POST /data/item ---");
            Map<String, Object> newItemData = new HashMap<>();
            newItemData.put("name", "New Learning Module");
            newItemData.put("durationMinutes", 60);
            newItemData.put("category", "Programming");

            String postResponse = sendPostRequest(requestFactory, BASE_CLOUD_RUN_ENDPOINT + "/data/item", newItemData);
            System.out.println("Response for POST /data/item: " + postResponse);
            System.out.println("-----------------------------------\n");

        } catch (IOException | GeneralSecurityException e) {
            System.err.println("An error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * Helper method to send a GET request.
     */
    private static String sendGetRequest(HttpRequestFactory requestFactory, String url) throws IOException {
        GenericUrl genericUrl = new GenericUrl(url);
        HttpRequest request = requestFactory.buildGetRequest(genericUrl);
        HttpResponse response = request.execute();
        return response.parseAsString();
    }

    /**
     * Helper method to send a POST request with a JSON body.
     */
    private static String sendPostRequest(HttpRequestFactory requestFactory, String url, Map<String, Object> bodyData) throws IOException {
        GenericUrl genericUrl = new GenericUrl(url);
        HttpContent content = new JsonHttpContent(JSON_FACTORY, bodyData);
        HttpRequest request = requestFactory.buildPostRequest(genericUrl, content);
        request.getHeaders().setContentType("application/json"); // Set content type explicitly
        HttpResponse response = request.execute();
        return response.parseAsString();
    }

    // You can add similar helper methods for PUT, DELETE, etc.
    // Example for PUT (similar to POST, just change buildPostRequest to buildPutRequest):
    // private static String sendPutRequest(HttpRequestFactory requestFactory, String url, Map<String, Object> bodyData) throws IOException {
    //     GenericUrl genericUrl = new GenericUrl(url);
    //     HttpContent content = new JsonHttpContent(JSON_FACTORY, bodyData);
    //     HttpRequest request = requestFactory.buildPutRequest(genericUrl, content); // Changed here
    //     request.getHeaders().setContentType("application/json");
    //     HttpResponse response = request.execute();
    //     return response.parseAsString();
    // }
}