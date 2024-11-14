#변수에 API 키 등등 넣음
import os
from openai import OpenAI

import streamlit as st

#키 세팅 과정
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.title("대화주제생성 GPT:robot_face:")

st.subheader("원하는 대화주제를 GPT에게 물어보세요!")

st.write("본 서비스는 팀스파르타 강의를 통해 Streamlit과 chatGPT API를 활용해 개발되었습니다.")

if st.button("예시 대화주제 보기"):
    st.write("상대방과 커플 유튜버를 한다면 어떤 콘텐츠가 좋을까요?")
    st.write("집에 가려는데 갑자기 비가 쏟아진다. 남사친/여사친은 우산이 없는 상황. 이때 연인이 역까지 우산을 씌워줘도 될까?")


level = st.select_slider(
    "짖궂음 정도를 정해주세요 휴먼, 저는 짖궂음 정도의 even함을 중요시하거덩요.",
    options=[
        "1",
        "2",
        "3",
        "4",
        "5",
    ],
)
st.write("짖궂음 단계", level, " 대화주제 만들어드릴게요(삐릭삐릿)")


txt = st.text_area(
    "대화주제 물어보기",
    "예) 감성, 밸런스게임(추천)",
)

if st.button('생성하기'): 
    # 프롬프트 구성 개선
    system_prompt = f"""
    다음 조건에 맞춰 대화 주제를 생성해주세요:
    1. 키워드: {txt}
    2. 짖궂음 레벨: {level} (1: 매우 순수, 5: 매우 짖궂음)
    3. 정확히 5개의 대화 주제를 생성
    4. 각 주제는 입력된 키워드와 짖궂음 레벨을 반드시 반영
    5. 질문 형식으로 작성
    6. 답변이나 설명 없이 질문만 제시
    7. 짖궂음 레벨이 높을수록 더 도발적이고 재치있는 질문 생성
    8. 각 질문은 번호를 매겨서 제시
    """

    user_prompt = f"키워드 '{txt}'와 짖궂음 레벨 {level}에 맞는 5개의 대화 주제를 만들어주세요."

    try:
        with st.spinner('생성 중입니다 휴먼,,,'):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="gpt-4o",  
                temperature=1.0,  # 창의성 부여
                max_tokens=500,  # 충분한 길이 확보
            )       

        result = chat_completion.choices[0].message.content
        st.write(result)

    except Exception as e:
        st.error(f"죄송합니다. 오류가 발생했습니다: {str(e)}")
