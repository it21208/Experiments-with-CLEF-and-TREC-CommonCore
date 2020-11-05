
package io.anserini.search.topicreader;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.SortedMap;
import java.util.TreeMap;

/**
 * Topic reader for queries in tsv format, such as the MS MARCO queries.
 *
 * <pre>
 * 174249 does xpress bet charge to deposit money in your account
 * 320792 how much is a cost to run disneyland
 * 1090270  botulinum definition
 * 1101279	do physicians pay for insurance from their salaries?
 * 201376 here there be dragons comic
 * 54544  blood diseases that are sexually transmitted
 * ...
 * </pre>
 */
public class TsvStringTopicReader extends TopicReader<String> {
  public TsvStringTopicReader(Path topicFile) {
    super(topicFile);
  }

  @Override
  public SortedMap<String, Map<String, String>> read(BufferedReader reader) throws IOException {
    SortedMap<String, Map<String, String>> map = new TreeMap<>();

    String line;
    while ((line = reader.readLine()) != null) {
      line = line.trim();
//      String[] arr = line.split("\\t");
      String[] arr = line.split(" ", 2);

      Map<String,String> fields = new HashMap<>();
      fields.put("title", arr[1].trim());
      map.put(arr[0], fields);
      
    }
    

    return map;
  }
}
