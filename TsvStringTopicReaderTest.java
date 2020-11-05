
package io.anserini.search.topicreader;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.Map;
import java.util.SortedMap;
import static org.junit.Assert.assertEquals;
import org.junit.Ignore;
import org.junit.Test;

@Ignore
public class TsvStringTopicReaderTest {

  @Test
  public void test() throws IOException {
    TopicReader<String> reader = new TsvStringTopicReader(
        Paths.get("src/main/resources/topics-and-qrels/topics.ntcir8en.eval.txt"));

    SortedMap<String, Map<String, String>> topics = reader.read();

    assertEquals(73, topics.keySet().size());
    assertEquals("ACLIA2-CS-0002", topics.firstKey());
    assertEquals("What is the relationship between the movie \"Riding Alone for Thousands of Miles\" and ZHANG Yimou?",
        topics.get(topics.firstKey()).get("title"));

    assertEquals("ACLIA2-CS-0100", topics.lastKey());
    assertEquals("Why did U.S. troops occupy Baghdad?", topics.get(topics.lastKey()).get("title"));
  }
}
