import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns
import pdfkit
import plotly.graph_objs as go
import plotly.express as px


# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# # Launch the Streamlit app in a headless Chrome browser
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run Chrome in headless mode
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver.get('http://localhost:8501')  # Replace with the URL of your Streamlit app

# # Capture the HTML content of the entire page
# html_content = driver.page_source

# # Save the HTML content to a file (optional)
# with open('output.html', 'w', encoding='utf-8') as file:
#     file.write(html_content)

# # Convert the HTML to PDF using your preferred method/library
# # ...

# # Close the browser
# driver.quit()


def run_app():
    st.sidebar.title("Whatsapp Chat Analyzer")

    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocess.preprocess(data)

        st.dataframe(df)

        # fetch unique users
        user_list = df['user'].unique().tolist()
        # user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

        if st.sidebar.button("Show Analysis"):

            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(num_links)




            # finding the busiest users in the group(Group level)
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x,new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                # col1, col2,col3 = st.columns(3)
                col1, col2 = st.columns([6, 4])

                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values,color='red')
                    ax.set_xlabel('Users')
                    ax.set_ylabel('Number of messages')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            # WordCloud
            st.title("Wordcloud")
            df_wc = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            plt.axis('off')
            st.pyplot(fig)

            # most common words
            most_common_df = helper.most_common_words(selected_user,df)

            fig,ax = plt.subplots()

            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks()
            ax.set_xlabel('frequency')
            ax.set_ylabel('Words')
            st.title('Most common words')
            st.pyplot(fig)
    

            # monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # daily timeline
            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            ax.set_xlabel('Day')
            ax.set_ylabel('Number of messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # activity map
            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='purple')
                ax.set_xlabel('Day')
                ax.set_ylabel('Number of messages')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='orange')
                ax.set_xlabel('Month')
                ax.set_ylabel('Number of messages')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)


            
            ####Heatmap####
            user_heatmap = helper.activity_heatmap(selected_user,df)
            def heat_map_gen(df : user_heatmap) -> go.Figure:
                return px.density_heatmap(user_heatmap,height=500)
            


            st.title("Weekly Activity Map")
            show_heatmap = heat_map_gen(user_heatmap)
            st.plotly_chart(show_heatmap)
            # user_heatmap = helper.activity_heatmap(selected_user,df)
            # fig,ax = plt.subplots()
            # ax = sns.heatmap(user_heatmap)
            # st.pyplot(fig)

            
            # emoji analysis
            emoji_df = helper.emoji_helper(selected_user,df)

            if len(emoji_df)==0:
                st.title('No emojis used by the user')
            else:    
                st.title("Emoji Analysis")

                col1,col2 = st.columns(2)

                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    fig = go.Figure(data=[go.Pie(labels=emoji_df[0].head(), values=emoji_df[1].head(), textinfo='label+value')])

                    # Set custom colors for the pie chart
                    # fig.update_traces(marker=dict(colors=colors))
                    fig.update_layout(margin=dict(t=0), width=560, height=400)

                    # Display the pie chart using Streamlit
                    st.plotly_chart(fig)
                    # fig,ax = plt.subplots()
                    # ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                    # st.pyplot(fig)


            
            #### Sentiment analysis

            sentiment,da,emo = helper.sentiment_analysis(selected_user,df)


            st.title("Sentiment Analysis")
            

            col1,col2 = st.columns(2)

        

            with col1:
                st.markdown(f""" 
                ## The Sentiment of the chat overall is ,{sentiment}
                
                ## Positive :smile: - {"{:.2f}".format(da[0])} %
                ## Negative :disappointed_relieved: - {"{:.2f}".format(da[1])} %
                ## Neutral :neutral_face: - {"{:.2f}".format(da[2])} %
                """)

            with col2:
                colors = ['#59CE72','#FF0000', '#616D76']

                # Create a Pie chart figure
                fig = go.Figure(data=[go.Pie(labels=emo, values=da, textinfo='label')])

                # Set custom colors for the pie chart
                fig.update_traces(marker=dict(colors=colors))
                fig.update_layout(margin=dict(t=0), width=560, height=400)

                # Display the pie chart using Streamlit
                st.plotly_chart(fig)
                # fig,ax = plt.subplots()

                # ax.pie(da,labels=emo)
              
                # st.pyplot(fig)
            
            # if st.sidebar.button("Download Result"):
            #     # Save the Streamlit app page as HTML
            #     html_content = st._get_streamlit_specific_html()
                
            #     # Convert the HTML to PDF using pdfkit
            #     pdfkit.from_string(html_content, 'output.pdf')
            #     st.success('PDF downloaded successfully!')


if __name__ == "__main__":
    run_app()




