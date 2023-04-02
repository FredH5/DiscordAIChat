FROM python
RUN pip install discord.py
RUN pip install openai
RUN mkdir /data && cd /data
COPY files/* /data/*
CMD python chatGPT.py
