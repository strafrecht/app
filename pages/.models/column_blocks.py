# Wagtail
from wagtail.core import blocks, fields
# 3rd Party
from wagtailcolumnblocks.blocks import ColumnsBlock
# Local
from .content_blocks import ContentBlocks

class ColumnBlocks(blocks.StreamBlock):
    """
    All the root level blocks you can use
    """
    column_2_1 = ColumnsBlock(
        # Blocks you want to allow within each column
        ContentBlocks(),
        # Two columns in admin, first twice as wide as the second
        ratios=(2, 1),
        # Used for grouping related fields in the streamfield field picker
        group="Columns",
        # 12 column frontend grid (this is the default, so can be omitted)
        grid_width=12,
        # Override the frontend template
        template='blocks/columnsblock.html',
    )

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        return context