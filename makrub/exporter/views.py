from rest_framework import views, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_pandas import PandasView
import pandas as pd
import json
import ast
import re

from core.models import RoomAnswer
from .serializers import RoomAnswerExportSerializer


class RoomAnswerExportView(PandasView):
    """
    Receive query string in url (my custom query string): ?room_id=<'id' of Room model>
    According to django-rest-pandas default, this view can also receive ?format=<csv, xlsx, ...>
    """
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerExportSerializer

    def filter_queryset(self, qs):
        # At this point, you can filter queryset based on self.request or other
        # settings (useful for limiting memory usage).  This function can be
        # omitted if you are using a filter backend or do not need filtering.
        return qs.filter(
            submitted=True, # only submitted answers
            guest_room_relation__room__id=int(self.request.query_params.get('room_id')), # room_id from query string
            guest_room_relation__room__user=self.request.user, # only room owner can get report
            )

    def transform_dataframe(self, df):
        # Warning !!! There is no 'encoding' parameter to set when initialize pd.DataFrame

        # django-rest-pandas auto use 'id' field as row index when initialize dataframe
        # So, we have to reset_index() first:
        df.reset_index(inplace=True)
        # Extract 'answer' column from dataframe as a new table
        answers = list(df.answer) # [ast.literal_eval(x) for x in df.answer]
        # New table:
        all_rows = []
        for indx, answers_list in enumerate(answers):
            # answers_list is list of answer(dict type)
            # 1 outer loop = 1 row = 1 guest
            row_data = {}

            # transform each row (1 dict) to column (each field in dict)
            for answer_indx, answer_dict in enumerate(answers_list):
                answer_num = answer_indx + 1
                each_question = answer_dict.get('question', None)
                each_answer = answer_dict.get('answerChoice', None) or answer_dict.get('answerText', None)
                row_data = {**row_data,
                            f'question_{answer_num}': each_question,
                            f'answer_{answer_num}': each_answer,
                        }
            all_rows.append(row_data)
        # Initialize dataframe from new table:
        df2 = pd.DataFrame(all_rows)
        # Concat old and new dataframe columns, then re-assign to 'df' variable:
        df = pd.concat([df, df2], axis=1, sort=False)
        # Pick and Reorder columns:
        cols = list(df.columns)
        ### Pick dynamic columns first
        extract_col_re = re.compile(r'(answer_)|(question_)')
        extract_col = []
        for col in cols:
            if extract_col_re.match(col):
                extract_col.append(col)
        ### Sort dynamic columns
        s1 = sorted(extract_col, key=lambda name: re.search(r'\d+', name).group(0))
        ### Pick static columns, add sorted dynamic columns, and sort all
        new_cols = ['guest_email', 'guest_first_name', 'guest_last_name'] + \
            s1 + \
            ['room_title', 'room_description', 'room_code', 'room_instructor']
        # Finalize df:
        df = df[new_cols]
        return df


class ForTest(generics.ListCreateAPIView):
    queryset = RoomAnswer.objects.all()
    serializer_class = RoomAnswerExportSerializer
