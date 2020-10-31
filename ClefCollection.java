package io.anserini.collection;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
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
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 *
 * @author pfb16181
 */
/**
 * A classic CLEF document collection.
 */
public class ClefCollection extends DocumentCollection<ClefCollection.Document> {

    private static final Logger LOG = LogManager.getLogger(ClefCollection.class);

    public ClefCollection(Path path) {
        this.path = path;
        this.allowedFileSuffix = new HashSet<>(Arrays.asList(".xml", ".tgz"));
    }

    @Override
    public FileSegment<ClefCollection.Document> createFileSegment(Path p) throws IOException {
        return new Segment(p);
    }

    /* This class works for both compressed
      * <code>tgz</code> files or uncompressed <code>xml</code> files.
     */
    public static class Segment extends FileSegment<ClefCollection.Document> {

        private final ClefCollection.Parser parser = new ClefCollection.Parser();
        private TarArchiveInputStream tarInput = null;
        private ArchiveEntry nextEntry = null;

        public Segment(Path path) throws IOException {
            super(path);
            if (this.path.toString().endsWith(".tgz")) {
                tarInput = new TarArchiveInputStream(new GzipCompressorInputStream(new FileInputStream(path.toFile())));
            }
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
                if (path.toString().endsWith(".xml")) {
                    atEOF = true;
                }
                throw e1;
            }
        }

        private void getNextEntry() throws IOException {
            nextEntry = tarInput.getNextEntry();
            if (nextEntry == null) {
                throw new NoSuchElementException();
            }
            // an ArchiveEntry may be a directory, so we need to read a next one.
            //   this must be done after the null check.
            if (nextEntry.isDirectory()) {
                getNextEntry();
            }
        }
    }

    
    
    
    public static class Document implements SourceDocument {

        private final ClefCollection.RawDocument raw;
        private String id;
        private String contents;

        // No public constructor; must use parser to create document.
        private Document(ClefCollection.RawDocument raw) {
            this.raw = raw;
        }

        @Override
        public String id() {
            return id;
        }

        @Override
        public String contents() {
            return contents;
        }

        @Override
        public String raw() {
            return contents;
        }

        @Override
        public boolean indexable() {
            return true;
        }

        public ClefCollection.RawDocument getRawDocument() {
            return raw;
        }
    }
    
    
    
    
    
    


    // We intentionally segregate the Anserini CLEFDocument from the parsed document below.
    /**
     * Raw container class for a document from New York Times Annotated Corpus.
     * This was originally distributed as part of the corpus as a class called
     * {@code NYTCorpusDocument}.
     */
    public static class RawDocument {

        /**
         * The GUID field specifies a an integer that is guaranteed to be unique
         * for every document in the corpus.
         */
        protected int guid;
        protected String articleTitle;
        protected String articleAbstract;
        protected String body;
        /* The file from which this object was read. */
        protected File sourceFile;

        public File getSourceFile() {
            return sourceFile;
        }

        public void setSourceFile(File sourceFile) {
            this.sourceFile = sourceFile;
        }

        public String getBody() {
            return body;
        }

        public void setBody(String body) {
            this.body = body;
        }

        public int getGuid() {
            return guid;
        }

        public void setGuid(int guid) {
            this.guid = guid;
        }

        public String getArticleTitle() {
            return articleTitle;
        }

        public void setArticleTitle(String articleTitle) {
            this.articleTitle = articleTitle;
        }

        public String getArticleAbstract() {
            return articleAbstract;
        }

        public void setArticleAbstract(String articleAbstract) {
            this.articleAbstract = articleAbstract;
        }


        private String ljust(String s, Integer length) {
            if (s.length() >= length) {
                return s;
            }
            length -= s.length();
            StringBuffer sb = new StringBuffer();
            for (Integer i = 0; i < length; i++) {
                sb.append(" ");
            }
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
            if (propertyValue != null) {
                propertyValue = propertyValue.toString().replaceAll("\\s+", " ").trim();
            }
            sb.append(ljust(propertyName + ":", 45) + propertyValue + "\n");
        }
        
    }

    /**
     * Parser for a document from New York Times Annotated Corpus. This was
     * originally distributed as part of the corpus as a class called
     * {@code NYTCorpusDocumentParser}.
     */
    public static class Parser {
        
        private static final String PMID_TEXT = "PMID";
        private static final String TITLE_TEXT = "ArticleTitle";
        private static final String ABSTRACT_TEXT = "Abstract";
        

        public ClefCollection.Document parseFile(BufferedReader bRdr, File fileName) throws IOException {
            ClefCollection.RawDocument raw = parseCLEFCorpusDocumentFromBufferedReader(bRdr, fileName);
            ClefCollection.Document d = new Document(raw);
            d.id = String.valueOf(raw.getGuid());
            d.contents = raw.getBody() == null ? "" : raw.getBody();
            return d;
        }

        /**
         * Parse an New York Times Document from a file.
         *
         * @param file the file from which to parse the document
         * @param validating true if the file is to be validated against the
         * NITF DTD and false if it is not. It is recommended that validation be
         * disabled, as all documents in the corpus have previously been
         * validated against the NITF DTD.
         * @return the parsed document, or null if an error occurs
         */
        public RawDocument parseNYTCorpusDocumentFromFile(File file, boolean validating) {
            org.w3c.dom.Document document = null;
            if (validating) {
                document = loadValidating(file);
            } else {
                document = loadNonValidating(file);
            }
            return parseCLEFCorpusDocumentFromDOMDocument(file, document);
        }

        /**
         * Parse a New York Time Document from BufferedReader. The parameter
         * `file` is used only to feed in other methods
         *
         * @param file the file from which to parse the document
         * @param bRdr the BufferedReader of file
         * @return the parsed document, or null if an error occurs
         */
        public RawDocument parseCLEFCorpusDocumentFromBufferedReader(BufferedReader bRdr, File file) {
            org.w3c.dom.Document document = loadFromBufferedReader(bRdr, file);
            return parseCLEFCorpusDocumentFromDOMDocument(file, document);
        }

        private org.w3c.dom.Document loadFromBufferedReader(BufferedReader bRdr, File file) {
            org.w3c.dom.Document document;
            StringBuffer sb = new StringBuffer();
            try {
                String line;
                while ((line = bRdr.readLine()) != null) {
                    sb.append(line + "\n");
                }
                String xmlData = sb.toString();
                xmlData = xmlData.replace("<!DOCTYPE nitf "
                        + "SYSTEM \"http://www.nitf.org/"
                        + "IPTC/NITF/3.3/specification/dtd/nitf-3-3.dtd\">", "");
                document = parseStringToDOM(xmlData, "UTF-8", file);
                return document;
            } catch (IOException e) {
                LOG.error("Error loading file " + file + ".");
            }
            return null;
        }

        public RawDocument parseCLEFCorpusDocumentFromDOMDocument(File file, org.w3c.dom.Document document) {
            RawDocument ldcDocument = new RawDocument();
            ldcDocument.setSourceFile(file);
            NodeList children = document.getChildNodes();
            for (int i = 0; i < children.getLength(); i++) {
                Node child = children.item(i);
                String name = child.getNodeName();
                if (name.equals(PMID_TEXT)) {
                    String docIdString = getAttributeValue(child, PMID_TEXT);
                    if (docIdString != null) {
                        try {
                            ldcDocument.setGuid(Integer.parseInt(docIdString));
                        } catch (NumberFormatException e) {
                            //e.printStackTrace();
                            LOG.error("Error parsing long from string " + docIdString + " in file " + ldcDocument.getSourceFile() + ".");
                        }
                    }
                } else if (name.equals(TITLE_TEXT)) {
                    String articleTitleString = getAttributeValue(child, TITLE_TEXT);
                    if (articleTitleString != null) {
                        ldcDocument.setArticleTitle(articleTitleString);
                    }
                } else if (name.equals(ABSTRACT_TEXT)) {
                    String abstractText = getAllText(child).trim();
                    if (abstractText != null) {
                        ldcDocument.setArticleAbstract(abstractText);
                    }   
                }
            }
            return ldcDocument;
        }

        
        
        private String getAttributeValue(Node node, String attributeName) {
            NamedNodeMap attributes = node.getAttributes();
            if (attributes != null) {
                Node attribute = attributes.getNamedItem(attributeName);
                if (attribute != null) {
                    return attribute.getNodeValue();
                }
            }
            return null;
        }
        
        
        private String getAllText(Node node) {
            List<Node> textNodes = getNodesByTagName(node, "AbstractText"); //#text
            StringBuffer sb = new StringBuffer();
            for (Node textNode : textNodes) {
                sb.append(textNode.getNodeValue().trim() + " ");
            }
            return sb.toString().trim();
        }
        
        
        private List<Node> getNodesByTagName(Node node, String tagName) {
            List<Node> matches = new ArrayList<Node>();
            recursiveGetNodesByTagName(node, tagName.toLowerCase(), matches);
            return matches;
        }
        
        
        
        private void recursiveGetNodesByTagName(Node node, String tagName, List<Node> matches) {
            String name = node.getNodeName();
            if (name != null && name.toLowerCase().equals(tagName)) {
                matches.add(node);
            }
            if (node.getChildNodes() != null
                    && node.getChildNodes().getLength() > 0) {
                for (int i = 0; i < node.getChildNodes().getLength(); i++) {
                    recursiveGetNodesByTagName(node.getChildNodes().item(i),
                            tagName, matches);
                }
            }
        }
        
        
        
        private org.w3c.dom.Document loadValidating(File file) {
            try {
                return getDOMObject(file.getAbsolutePath(), true);
            } catch (SAXException e) {
                //e.printStackTrace();
                LOG.error("Error parsing digital document from file "
                        + file + ".");
            } catch (IOException e) {
                //e.printStackTrace();
                LOG.error("Error parsing digital document from file "
                        + file + ".");
            } catch (ParserConfigurationException e) {
                //e.printStackTrace();
                LOG.error("Error parsing digital document from file "
                        + file + ".");
            }
            return null;
        }

        private org.w3c.dom.Document getDOMObject(String filename, boolean validating)
                throws SAXException, IOException, ParserConfigurationException {
            // Create a builder factory
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            if (!validating) {
                factory.setValidating(validating);
                factory.setSchema(null);
                factory.setNamespaceAware(false);
            }
            DocumentBuilder builder = factory.newDocumentBuilder();
            // Create the builder and parse the file
            org.w3c.dom.Document doc = builder.parse(new File(filename));
            return doc;
        }

        private org.w3c.dom.Document loadNonValidating(File file) {
            org.w3c.dom.Document document;
            StringBuffer sb = new StringBuffer();
            try {
                BufferedReader in = new BufferedReader(new InputStreamReader(
                        new FileInputStream(file), "UTF8"));
                String line = null;
                while ((line = in.readLine()) != null) {
                    sb.append(line + "\n");
                }
                String xmlData = sb.toString();
                xmlData = xmlData.replace("<!DOCTYPE nitf "
                        + "SYSTEM \"http://www.nitf.org/"
                        + "IPTC/NITF/3.3/specification/dtd/nitf-3-3.dtd\">", "");
                document = parseStringToDOM(xmlData, "UTF-8", file);
                in.close();
                return document;
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
                LOG.error("Error loading file " + file + ".");
            } catch (FileNotFoundException e) {
                e.printStackTrace();
                LOG.error("Error loading file " + file + ".");
            } catch (IOException e) {
                e.printStackTrace();
                LOG.error("Error loading file " + file + ".");
            }
            return null;
        }

        private org.w3c.dom.Document parseStringToDOM(String s, String encoding, File file) {
            try {
                DocumentBuilderFactory factory = DocumentBuilderFactory
                        .newInstance();
                factory.setValidating(false);
                InputStream is = new ByteArrayInputStream(s.getBytes(encoding));
                org.w3c.dom.Document doc = factory.newDocumentBuilder().parse(is);
                is.close();
                return doc;
            } catch (SAXException e) {
                e.printStackTrace();
                LOG.error("Exception processing file " + file + ".");
            } catch (ParserConfigurationException e) {
                e.printStackTrace();
                LOG.error("Exception processing file " + file + ".");
            } catch (IOException e) {
                e.printStackTrace();
                LOG.error("Exception processing file " + file + ".");
            }
            return null;
        }

    }

}
