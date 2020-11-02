package io.anserini.collection;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.lang.*;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.NoSuchElementException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.apache.commons.compress.archivers.ArchiveEntry;
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream;
import org.apache.commons.compress.compressors.gzip.GzipCompressorInputStream;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

//@github author pfb16181 => Alexandros Ioannidis
public class ClefCollection extends DocumentCollection<ClefCollection.Document> {
    private static final Logger LOG = LogManager.getLogger(ClefCollection.class);
    public ClefCollection(Path path) {
        this.path = path;
        this.allowedFileSuffix = new HashSet<>(Arrays.asList(".xml", ".tgz"));
    }

    @Override
    public FileSegment<ClefCollection.Document> createFileSegment(Path p) throws IOException { return new Segment(p); }
    public static class Segment extends FileSegment<ClefCollection.Document> { // <code>tgz</code> files or uncompressed <code>xml</code> files.
        private final ClefCollection.Parser parser = new ClefCollection.Parser();
        private TarArchiveInputStream tarInput = null;
        private ArchiveEntry nextEntry = null;
        public Segment(Path path) throws IOException {
            super(path);
            if (this.path.toString().endsWith(".tgz")) {tarInput = new TarArchiveInputStream(new GzipCompressorInputStream(new FileInputStream(path.toFile())));}
        }

        @Override
        protected void readNext() throws IOException, NoSuchElementException {
            try {
                if (path.toString().endsWith(".tgz")) {
                    getNextEntry();
                    bufferedReader = new BufferedReader(new InputStreamReader(tarInput, "UTF-8"));
                    File file = new File(nextEntry.getName()); // this is actually not a real file, only to match the method in Parser
                    bufferedRecord = parser.parseFile(bufferedReader, file);
                } else {
                    bufferedReader = new BufferedReader(new InputStreamReader(new FileInputStream(path.toFile()), "UTF-8"));
                    bufferedRecord = parser.parseFile(bufferedReader, path.toFile());
                    atEOF = true; // if it is a xml file, the segment only has one file, boolean to keep track if it's been read.
                }
            } catch (IOException e1) {
                if (path.toString().endsWith(".xml")) { atEOF = true; }
                throw e1;
            }
        }

        private void getNextEntry() throws IOException {
            nextEntry = tarInput.getNextEntry();
            if (nextEntry == null) { throw new NoSuchElementException(); }
            if (nextEntry.isDirectory()) { getNextEntry(); }   // an ArchiveEntry may be a directory, so we need to read a next one. this must be done after the null check.
        }
    }
    
    public static class Document implements SourceDocument {
        private final ClefCollection.RawDocument raw;
        private String id;
        private String contents;
        private Document(ClefCollection.RawDocument raw) { this.raw = raw; } // No public constructor; must use parser to create document.
        @Override
        public String id() {return id; }
        @Override
        public String contents() { return contents; }
        @Override
        public String raw() { return contents; }
        @Override
        public boolean indexable() { return true; }
        public ClefCollection.RawDocument getRawDocument() { return raw; }
    }
    
    public static class RawDocument {
        protected int guid;   // The GUID field specifies an integer that is guaranteed to be unique for every document in the corpus.
        protected String articleTitle;
        protected String articleAbstract;
        protected String body;
        protected File sourceFile; // The file from which this object was read.
        public File getSourceFile() { return sourceFile; }
        public void setSourceFile(File sourceFile) { this.sourceFile = sourceFile; }
        public String getBody() { return getArticleTitle() + " " + getArticleAbstract(); }
        public void setBody(String body) { this.body = body; }
        public int getGuid() { return guid; }
        public void setGuid(int guid) { this.guid = guid; }
        public String getArticleTitle() { return articleTitle; }
        public void setArticleTitle(String articleTitle) { this.articleTitle = articleTitle; }
        public String getArticleAbstract() { return articleAbstract; }
        public void setArticleAbstract(String articleAbstract) { this.articleAbstract = articleAbstract; }

        private String ljust(String s, Integer length) {
            if (s.length() >= length) { return s; }
            length -= s.length();
            StringBuffer sb = new StringBuffer();
            for (Integer i = 0; i < length; i++) { sb.append(" "); }
            return s + sb.toString();
        }
             
        @Override
        public String toString() {
            StringBuffer sb = new StringBuffer();
            appendProperty(sb, "guid", guid);
            appendProperty(sb, "articleTitle", articleTitle);
            appendProperty(sb, "articleAbstract", articleAbstract);
            appendProperty(sb, "body", body);
            return sb.toString();
        }
        
        private void appendProperty(StringBuffer sb, String propertyName, Object propertyValue) {
            if (propertyValue != null) { propertyValue = propertyValue.toString().replaceAll("\\s+", " ").trim(); }
            sb.append(ljust(propertyName + ":", 45) + propertyValue + "\n");
        }
    }

    public static class Parser {
        private static final String PMID_TEXT = "PMID";
        private static final String TITLE_TEXT = "ArticleTitle";
        private static final String ABSTRACT_TEXT = "Abstract";
        public ClefCollection.Document parseFile(BufferedReader bRdr, File fileName) throws IOException {
            ClefCollection.RawDocument raw = parseCLEFCorpusDocumentFromBufferedReader(bRdr, fileName);
            ClefCollection.Document d = new Document(raw);
            d.id = String.valueOf(raw.getGuid());
            if (raw.getBody() == null) { d.contents = ""; } 
            else { d.contents = raw.getBody(); }
            return d;
        }

        public RawDocument parseCLEFCorpusDocumentFromFile(File file, boolean validating) {
            org.w3c.dom.Document document = null;
            if (validating) {  document = loadValidating(file); } 
            else { document = loadNonValidating(file); }
            return parseCLEFCorpusDocumentFromDOMDocument(file, document);
        }

        public RawDocument parseCLEFCorpusDocumentFromBufferedReader(BufferedReader bRdr, File file) {
            org.w3c.dom.Document document = loadFromBufferedReader(bRdr, file);
            return parseCLEFCorpusDocumentFromDOMDocument(file, document);
        }

        private org.w3c.dom.Document loadFromBufferedReader(BufferedReader bRdr, File file) {
            org.w3c.dom.Document document;
            StringBuffer sb = new StringBuffer();
            try {
                String line;
                while ((line = bRdr.readLine()) != null) { sb.append(line + "\n"); }
                String xmlData = sb.toString();
                xmlData = xmlData.replace(" standalone=\"no\"", "");
                xmlData = xmlData.replace("<!DOCTYPE PubmedArticleSet " + "PUBLIC \"-//NLM//DTD PubMedArticle, 1st January 2019//EN\" " + "\"https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd"+ "\">", "");
                document = parseStringToDOM(xmlData, "UTF-8", file);
                return document;
            } catch (IOException e) { LOG.error("Error loading file " + file + "."); }
            return null;
        }
        
        public RawDocument parseCLEFCorpusDocumentFromDOMDocument(File file, org.w3c.dom.Document document) {
            RawDocument ldcDocument = new RawDocument();
            ldcDocument.setSourceFile(file);
//            NodeList children = document.getChildNodes();
            String docIdString = "";
            NodeList children = document.getElementsByTagName(PMID_TEXT);
            for (int i = 0; i < children.getLength(); i++) {
                Node child = children.item(i);
                String name = child.getNodeName();
                if (name.equals(PMID_TEXT)) {
                    docIdString = child.getTextContent();
                    if (docIdString != null) {
                        try { ldcDocument.setGuid(Integer.parseInt(docIdString)); } 
                        catch (NumberFormatException e) {LOG.error("Error parsing long from string " + docIdString + " in file " + ldcDocument.getSourceFile() + ".");}
                    }
                } 
            }
//            LOG.info(String.format("docIdString = " + docIdString));
            
            String articleTitleString = "";
            NodeList children2 = document.getElementsByTagName(TITLE_TEXT);
            for (int i = 0; i < children2.getLength(); i++) {
                Node child = children2.item(i);
                String name = child.getNodeName();
                if (name.equals(TITLE_TEXT)) {
                    articleTitleString = child.getTextContent();
                    if (articleTitleString != null) { ldcDocument.setArticleTitle(articleTitleString); }
                }
            }
//            LOG.info(String.format("title = " + articleTitleString));
               
            
            String articleAbstractString = "";
            NodeList children3 = document.getElementsByTagName(ABSTRACT_TEXT);
            for (int i = 0; i < children3.getLength(); i++) {
                Node child = children3.item(i);
                String name = child.getNodeName();
                if (name.equals("Abstract")) {
                    articleAbstractString += " " + child.getTextContent();
//                    String abstractText = getAllText(child).trim();
                    if (articleAbstractString != null) { ldcDocument.setArticleAbstract(articleAbstractString); }   
                }
            }
//            LOG.info(String.format("abstract = " + articleAbstractString));
//            System.exit(0);
            return ldcDocument;
        }

        private String getAllText(Node node) {
            List<Node> textNodes = getNodesByTagName(node, "AbstractText"); //#text
            StringBuffer sb = new StringBuffer();
            for (Node textNode : textNodes) { sb.append(textNode.getNodeValue().trim() + " "); }
            return sb.toString().trim();
        }

        private List<Node> getNodesByTagName(Node node, String tagName) {
            List<Node> matches = new ArrayList<Node>();
            recursiveGetNodesByTagName(node, tagName.toLowerCase(), matches);
            return matches;
        }

        private void recursiveGetNodesByTagName(Node node, String tagName, List<Node> matches) {
            String name = node.getNodeName();
            if (name != null && name.toLowerCase().equals(tagName)) { matches.add(node); }
            if (node.getChildNodes() != null && node.getChildNodes().getLength() > 0) {
                for (int i = 0; i < node.getChildNodes().getLength(); i++) {  recursiveGetNodesByTagName(node.getChildNodes().item(i), tagName, matches); }
            }
        }
        
        private org.w3c.dom.Document loadValidating(File file) {
            try { return getDOMObject(file.getAbsolutePath(), true); } 
            catch (SAXException e) { LOG.error("Error parsing digital document from file " + file + "."); } 
            catch (IOException e) { LOG.error("Error parsing digital document from file " + file + "."); } 
            catch (ParserConfigurationException e) { LOG.error("Error parsing digital document from file " + file + "."); }
            return null;
        }

        private org.w3c.dom.Document getDOMObject(String filename, boolean validating) throws SAXException, IOException, ParserConfigurationException {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance(); // Create a builder factory
            if (!validating) {
                factory.setValidating(validating);
                factory.setSchema(null);
                factory.setNamespaceAware(false);
            }
            DocumentBuilder builder = factory.newDocumentBuilder();
            org.w3c.dom.Document doc = builder.parse(new File(filename)); // Create the builder and parse the file
            return doc;
        }

        private org.w3c.dom.Document loadNonValidating(File file) {
            org.w3c.dom.Document document;
            StringBuffer sb = new StringBuffer();
            try {
                BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(file), "UTF8"));
                String line = null;
                while ((line = in.readLine()) != null) { sb.append(line + "\n"); }
                String xmlData = sb.toString();
                xmlData = xmlData.replace(" standalone=\"no\"", "");
                xmlData = xmlData.replace("<!DOCTYPE PubmedArticleSet " + "PUBLIC \"-//NLM//DTD PubMedArticle, 1st January 2019//EN\" " + "\"https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd"+ "\">", "");
                document = parseStringToDOM(xmlData, "UTF-8", file);
                in.close();
                return document;
            } catch (UnsupportedEncodingException e) { 
                LOG.error("Error loading file " + file + ".");
            } catch (FileNotFoundException e) {
                LOG.error("Error loading file " + file + ".");
            } catch (IOException e) {
                LOG.error("Error loading file " + file + ".");
            }
            return null;
        }

        private org.w3c.dom.Document parseStringToDOM(String s, String encoding, File file) {
            try {
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                factory.setValidating(false);
                byte[] s_getBytes =  s.getBytes(encoding);
                ByteArrayInputStream is = new ByteArrayInputStream(s_getBytes);
                org.w3c.dom.Document doc = factory.newDocumentBuilder().parse(is);
                is.close();
                return doc;
            } catch (SAXException e) { LOG.error("Exception processing file " + file + "."); } 
            catch (ParserConfigurationException e) { LOG.error("Exception processing file " + file + "."); } 
            catch (IOException e) { LOG.error("Exception processing file " + file + "."); }
            return null;
        }   
    }
}
