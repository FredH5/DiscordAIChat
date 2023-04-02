FROM python
RUN pip install discord.py
RUN pip install openai
RUN mkdir /data && cd /data
COPY chatGPT.py /data/chatGPT.py
CMD python chatGPT.py
