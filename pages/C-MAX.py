import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain_community.document_loaders import PyPDFLoader

openai_api_key = "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"

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        st.write(message.content)
        
        # if i % 2 == 0:
            # st.write(user_template.replace(
            #     "{{MSG}}", message.content), unsafe_allow_html=True)
            # st.write(message.content)
        # else:
            # st.write(bot_template.replace(
            #     "{{MSG}}", message.content), unsafe_allow_html=True)
            # st.write(message.content)
footer_html = """
    <hr style="border: none; border-top: 1px solid #555; margin-top: 2em; margin-bottom: 0;" />
    <p style="font-size: 0.8em; color: #777; text-align: center;">Powered by: Valorize</p>
    """

def main():
    load_dotenv()
    st.set_page_config(page_title="C-MAX",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # if "conversation" not in st.session_state:
        # st.session_state.conversation = None
    # if "chat_history" not in st.session_state:
        # st.session_state.chat_history = None

    

    st.title("C-MAX")
    st.caption("Streamlining resilience....")
    # st.header("Relevant content")
    
    user_question = st.text_input("Please note this is a Beta vesion. The model still under development!")
    if user_question:
        handle_userinput(user_question)
        

    
    with st.sidebar:
        st.image("step.png",width=300)
        # openai_api_key = st.secrets["openai_api_key"]
        st.markdown(footer_html, unsafe_allow_html=True)
        # pdf_docs = PdfReader('collection.pdf')
        # open('collection.pdf','rb')
        # st.file_uploader(
        #     "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
            
    raw_text = "Table of Contents\n5.3.3 Monitoring and Review Phase \n5.3.3.1 Monitoring, Measurement and Evaluation\n5.3.3.2 Internal Audit and Review\n5.3.3.3 Management review\n5.3.3.4 Analysis of business continuity tests\n5.3.4 Maintenance and Improvement Phase\n5.3.4.1 Compliance and Corrective Actions\n5.3.4.2 Continuous Improvement\nBusiness Continuity Performance Indicators\nBusiness Continuity Success Factors\nTable of Definitions\nTable of  Abbreviations\nAppendix 2. Guideline Objectives\nThis guideline will contribute to enabling entities to :\n4. Continuity of critical services and procedures \nduring accidents and crises.\n5. Comply with regulatory requirements.\n6. Raise the level of integration between \ngovernment entities and enhance resilience \nand resilience at the national level.1. Have knowledge and understanding of \nthe applying the business continuity \nmanagement standards for digital \ngovernment in government entities.\n2. Help to reduce the likelihood or impact of \ninterruptions to the services.\n3. Raise readiness by preparing, responding \nto and recovering from interruptions.\n3. Guideline Scope\nEnhance the resilience ofgovernment entities torespond toany disruptions and enable\nthem torecover their main operations and services through guiding government entities,\nsuppliers and operators ofdigital government services toimplement and maintain an\neffective management system that provides the necessary capabilities tocontinue the\nbusiness operations while facing any disruption, aswell ascomply with legal and\nregulatory requirements .\nAdditionally, this guideline provides guidance toenhance business continuity practices in\ngovernment entities asperthemethodology ofPlan, Do,Check, Act(PDCA), asshown in\ntheFigure (1)below :\nFigure 1: Business continuity system sequence\n4. Target Audience\nThe recommendations contained in this document can be used by\ngovernment entities that provide digital services and products and operators\nregardless oftheir type, size and nature .The applicability ofthe recommendations\nwill depend onthe entity's operating environment, level ofcomplexity and number\nofitsgeographical locations .\nStakeholders\nBusiness Continuity Management\nStakeholders\nBusiness Continuity Requirements 5.1Key principles forBCM development\nInorder todevelop aneffective and successful BCMS, it’snecessary tofirst\nunderstand the entity, the work environment and the operations processes,\nunderstand theneeds and expectations ofstakeholders, and define thescope ofwork\nofthe BCMS .Then define the external and internal business obligations and\nsuppliers, establish and develop aBCM policy, define the authorities ,roles and\nresponsibilities, then identify opportunities, risks and develop plans todeal with\nthem, determine the strategic and operational objectives ofthe entity and develop\nplans toachieve them .\nThe basic principles ofdeveloping aBCMS includes identifying efficiencies, resources\nand effective ways tosupport the implementation ofabusiness continuity system .It\nalso includes risk assessment, business interruption impact analysis, incident\nresponse strategies and solutions, and operational recovery plans .Italso involves\nmonitoring, auditing, verification and performance appraisal .Finally, theprocesses of\ndevelopment, continuous improvement and correction .5. Guideline Statement\nKey principles for BCM development\nUnderstanding the working \nenvironment and stakeholders ’ \nexpectations and involved partiesLearning about the legislative and \nregulatory ecosystem and its \nrequirements\nDetermining the scope of work of \nbusiness  continuity system in the \nGovernment entity ’s Determining the internal and external \nbusiness commitments, and the \nGovernment entity ’s strategic objectives \nFigure 2: Key Principles for Developing Business Continuity Management 5.2Business Continuity Management System Methodology\nBased onBCMS inDigital Government issued byDGA, the methodology ofPLAN,\nDO, CHEC K,and ACT (PDCA) must befollowed, asshown inFigure (3)below :\n5.2.1Plan (Establishment)\nBCM planning start with understanding the context ofthe Government entity ’s\nwork, and the scope ofitsbusiness continuity system based onthe Government entity ’s\ninternal and external business obligations related toitsobjectives and strategic\nvision tobuild business continuity policies and strategies, and clarifying itsobjectives,\ncontrols, procedures and roles and responsibilities ofstakeholders, astheir results\nsupport and develop the Government entity ’spolicy and objectives .Itshould also be\nnoted that the Business Continuity System objectives consistent with the Government\nentity ’sstrategy, taking into account the context and organizational scope ofthe\nGovernment entity ’s,be shared with stakeholders within the system, and be\ncontinuously monitored and updated .\n5.2.2Do(Processes &Operation)\nBased onthe outputs ofthe Plan phase, the Do phase isthen launched, which\nconsists of:\n•Analyze the impact ofthe digital processes, procedures and services interruption to\ndetermine the level ofcriticality according toaspecific timeframe toprioritize .And\ndetermine the resources required for its continuity and internal and external\ndependencies .\n•Build the necessary strategies and solutions toachieve the goals and objectives of\nrestoring services and businesses and addressing the risks that may cause them tobe\ndisrupted .\n•Identify associated risks toset recovery priorities ,incident response and crisis\nmanagement .\n•Build business continuity orrecovery plans based onadetailed analysis ofthe impact\nofthedisruption ofthese processes orprocedures .Maintaining and improving \nperformance\nMonitoring & Auditing\nand continuous testing\nWork on the requirements \nof business continuity and \noperation\nSpecify requirements\nBusiness Continuity 5.2.4Act(Improvement)\nDuring this phase, gaps and shortcomings identified during the Check phase are\ncorrected for the purpose ofensuring the effectiveness and alignment ofthe\nGovernment entity ’sbusiness continuity system with the Government entity ’s\noperational and strategic objectives .5.2.3Check (Monitoring &Review)\nToensure that the planned and implemented policies, plans, and strategies for\nbusiness continuity arealigned with theGovernment entity ’sobjectives and priority\ntorestore itscritical processes orprocedures, theBusiness Continuity system subject\nto continuous verification through periodic review, continuous execution\noftests and various scenarios toidentify gaps and deficiencies .and training and\nawareness ofthose concerned with theBusiness Continuity Management system General scope of business continuity5.3.1Planning Phase\n5.3.1.1Government Entity regulatory scope\nThe first phase ofthe system starts with providing the necessary requirements and\ndefining the Government entity ’s regulatory scope, including the context and\nregulatory scope ofthe Business Continuity System .This isachieved bydefining\nthe capabilities and the scope ofthe BCMS scope, taking into account the internal and\nexternal framework related to the Government entity ’s requirements, legal\nand legislative requirements aswell asstakeholders"
                
                # get_pdf_text(pdf_docs)

                # get the text chunks
    text_chunks = get_text_chunks(raw_text)

                # create vector store
    vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
    st.session_state.conversation = get_conversation_chain(vectorstore)



if __name__ == '__main__':
    main()
